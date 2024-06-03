import React from "react";
import { Card } from "primereact/card";
import { Button } from "primereact/button";


const Detail = () => {

    return (
        <div className="p-list contentpage" style={{ marginTop: 20, marginBottom: 15 }}>
            <Card title="Objectives" className="contentcard">
                <div style={{ lineHeight: 1.4, fontSize: 18 }}>
                    <p> i4Q Project aims to provide an IoT-based Reliable
                        Industrial Data Services (RIDS), a complete suite
                        consisting of 22 i4Q Solutions, able to manage the
                        huge amount of industrial data coming from cheap
                        cost-effective, smart, and small size interconnected
                        factory devices for supporting manufacturing online
                        monitoring and control. The i4Q Framework will guarantee
                        data reliability with functions grouped into five basic
                        capabilities around the data cycle: sensing, communication,
                        computing infrastructure, storage, and analysis and optimization.
                        i4Q RIDS will include simulation and optimization tools for manufacturing
                        line continuous process qualification, quality diagnosis, reconfiguration and
                        certification for ensuring high manufacturing efficiency, leading to an
                        integrated approach to zero-defect manufacturing.
                    </p>
                    <p>
                        The i4Q RIDS will be demonstrated in 6 Uses Cases
                        from relevant industrial sectors and representing
                        two different levels of the manufacturing process:
                        machine tool providers and production companies.
                        i4Q pan-European consortium entails Industrial
                        partners: WHIRLPOOL (White goods manufacturer),
                        BIESSE (Wood industrial equipment), FACTOR
                        (Metal machining), RIASTONE (Ceramic pressing),
                        FARPLAS (Plastic injection) and FIDIA
                        (Metal industrial equipment); Implementers:
                        TIAG (Industrial Communication Protocols and
                        Standards), CESI (Machine tools, Advanced
                        Materials, Micro-technology) and AIMPLAS
                        (Thermoplastic and thermosetting plastic
                        materials); Technology Providers: IBM
                        (Information Technologies Company),
                        ENGINEERING (Software and Services Company),
                        ITI (Information Technologies Institute),
                        KNOWLEDGEBIZ (Information Systems Company),
                        EXOS (Operations Consulting Company);
                        R&D partners: CERTH (Research Institute),
                        IKERLAN (Technological Centre),
                        BIBA (Research Institute), UPV (University),
                        TUBERLIN (University), UNINOVA (Research Institute);
                        Specialist partners: FUNDINGBOX (Exploitation),
                        INTEROP-VLAB (Dissemination), DIN (Standardisation),
                        LIF (Legal).
                    </p>
                </div>
                <div style={{ textAlign: 'right', marginBottom: 0 }}>
                    <Button label="More info" icon="pi pi-plus" className="p-button-raised" />
                </div>
            </Card>
        </div>
    )
}
export default Detail;