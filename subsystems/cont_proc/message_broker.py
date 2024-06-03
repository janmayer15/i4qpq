# from dllFix import find_dll
# find_dll()  

import pandas as pd
from confluent_kafka import SerializingProducer, DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from confluent_kafka.serialization import StringSerializer, StringDeserializer
from confluent_kafka.cimpl import KafkaException, KafkaError
from confluent_kafka.error import SerializationError
import struct as _struct
from json import loads, dumps
from math import inf
from time import time

class Serializer():  
    def __init__(self, codec='utf_8'):
        self.codec = codec

    def __call__(self, obj, ctx):
        if obj is None:
            return None
        try:
            return dumps(obj).encode(self.codec)
        except _struct.error as e:
            raise SerializationError(str(e))
            
class Deserializer():  
    def __init__(self, codec='utf_8'):
        self.codec = codec

    def __call__(self, obj, ctx):
        if obj is None:
            return None
        try:
            return loads(obj.decode(self.codec))
        except _struct.error as e:
            raise SerializationError(str(e))

class Producer:
    def __init__(self, host_ip,  message_format='json', schema=None):
        
        if message_format == 'json':  
            serializer = Serializer()
            
        elif message_format == 'avro':
            schema_str = schema  
            
            schema_registry_conf = {'url': 'https://'+host_ip+':8081',
                                    
                                    'ssl.ca.location': './Certificates/client/CARoot.pem',
                                    'ssl.key.location': './Certificates/client/key.pem',
                                    'ssl.certificate.location': './Certificates/client/certificate.pem'}
            
            schema_registry_client = SchemaRegistryClient(schema_registry_conf)
            serializer = AvroSerializer(schema_registry_client, schema_str)
        
        producer_conf = {'bootstrap.servers': host_ip+':9092,'+host_ip+':9093,'+host_ip+':9094',
                        'key.serializer': StringSerializer('utf_8'),
                        'value.serializer': serializer,
                        'queue.buffering.max.messages': 1000000,
                        'message.max.bytes': 10485760,
                        
                        'security.protocol': 'SSL',
                        'ssl.ca.location': './Certificates/client/CARoot.pem',
                        'ssl.key.location': './Certificates/client/key.pem',
                        'ssl.certificate.location': './Certificates/client/certificate.pem'}

        self.producer = SerializingProducer(producer_conf)  

    def delivery_report(self, err, msg):
        if err is not None:
            print("Delivery failed for Machine record {}: {}".format(msg.key(), err))
        else:
            print('Order record {} successfully produced to {} [{}] at offset {}'.format(
                msg.key(), msg.topic(), msg.partition(), msg.offset()))

    def produce(self, topic, message, key=1):
        try:
            if type(message) == dict:
                df_dict = [message]
            else:
                df_dict = message.to_dict('records')
                
            for row in df_dict:
                try:
                    self.producer.produce(topic=topic, key=str(key) , value=row)
                    self.producer.poll(0.0)
                except KeyboardInterrupt:
                    break
        except KeyboardInterrupt:
            pass
            
        self.producer.flush()
            
class Consumer:
    def __init__(self, host_ip, group, message_format='json'):
        
        if message_format == 'json':
            deserializer = Deserializer()
            
        elif message_format == 'avro':
            schema_registry_conf = {'url': 'https://'+host_ip+':8081',
                                    
                                    'ssl.ca.location': './Certificates/client/CARoot.pem',
                                    'ssl.key.location': './Certificates/client/key.pem',
                                    'ssl.certificate.location': './Certificates/client/certificate.pem'}
                                    
            schema_registry_client = SchemaRegistryClient(schema_registry_conf)
            deserializer = AvroDeserializer(schema_registry_client)
        
        self.topic = ''
        self.index = None
        self.consumer_conf = {'bootstrap.servers': host_ip+':9092,'+host_ip+':9093,'+host_ip+':9094',
                            'key.deserializer': StringDeserializer('utf_8'),
                            'value.deserializer': deserializer,
                            'group.id': str(group),
                            'auto.offset.reset': 'earliest',
                            'enable.auto.commit':'True',
                            'auto.commit.interval.ms': 500,
                            
                            'security.protocol': 'SSL',
                            'ssl.ca.location': './Certificates/client/CARoot.pem',
                            'ssl.key.location': './Certificates/client/key.pem',
                            'ssl.certificate.location': './Certificates/client/certificate.pem'}
                                
        self.consumer = DeserializingConsumer(self.consumer_conf)

    def latest_assign(self, consumer, partitions):
        for p in partitions:
            _, last_offset = consumer.get_watermark_offsets(p)
            p.offset = last_offset-self.index
        consumer.assign(partitions)  
    

    def consume(self, topic, limit=inf, consume_timeout=2, index=None, none_msg_timeout=2):
        
        try:  
            if self.topic != topic or self.index != index:
                self.index = index    
                self.topic = topic
                
                self.consumer.unsubscribe()
                
                if self.index != None:
                    self.consumer.subscribe([topic], on_assign=self.latest_assign)
                else: 
                    self.consumer.subscribe([topic])

            msg_list = []
            lim = limit 
            last_msg_time = inf
            consume_start_time = time() 
            
            try:
                while lim:
                    if time()-consume_start_time > consume_timeout: break    
                
                    msg = self.consumer.poll(0.0)
                    if msg is None :
                        if time()-last_msg_time > none_msg_timeout: break                                       
                        else: continue
                        
                    elif msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            print('%% %s [%d] reached end at offset %d\n' % (msg.topic(), msg.partition(), msg.offset()))
                        else:
                            raise KafkaException(msg.error()) 
                            
                    else:        
                        val = msg.value()
                        if val is not None:
                            consume_timeout = inf
                            if type(val) is list: val = val[0]
                            msg_list.append(val)           
                            last_msg_time = time()
                            lim -= 1
                            
            except KeyboardInterrupt:
                print("INTERRUPTED")
                pass

            except:
                print("INTERRUPTED")
                pass
        
            self.consumer.commit()
            
            # if limit == 1:
            #     if bool(msg_list): return msg_list[0]
            #     else: return {}     
            # else:
            #     df = pd.DataFrame(msg_list)
            #     return df
            df = pd.DataFrame(msg_list)
            return df

        except:
            print("CLOSED")
            self.close()
            return None
        
    def close(self):
        self.consumer.close()





