### SiSEG: Auto Semantic Annotation Service to Integrate Smart Energy Data


* SiSEG requires 2 inputs in order to successfully carry out the automated annotation process:
    * an ontology file (Turtle format)
    * raw data which is about to be annotated (XML, JSON or CSV)


* annotation result is returned in various forms:
    * JSON-LD
    * Turtle (RDF graph)
    * OWL (XML)

* An API is developed for the tool. API's description is available in the following link:
    * https://app.swaggerhub.com/apis-docs/ahnazary/SiSEG/0.1#/

###### In the following, a few examples are depicted for better clarification. 
***


#### Example 1 :
* Raw data with CSV format (input):
```json
{
"id": "Zone:01",
    "type": "Zone",
    "inBuilding": {
        "type": "Relationship",
        "value": "Building:01"
    },
"inFloor": {
        "type": "Relationship",
        "value":"Floor:01"
    },
"inRoom": {
        "type": "Relationship",
        "value": [
            "Room:01",
            "Room:02"
        ]
    },
"containOf": {
        "type": "Relationship",
        "value": [
            "Zone:02",
            "Zone:03"
        ]
    }
}

```
* Output or the annotation result (JSON-LD)
```json
{
    "@context": {
        "inBuilding": "https://sargon-n5geh.netlify.app/ontology/1.0/object_properties/in_building",
        "inFloor": "https://sargon-n5geh.netlify.app/ontology/1.0/object_properties/in_floor",
        "inRoom": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Room",
        "containOf": "https://sargon-n5geh.netlify.app/ontology/1.0/object_properties/contain_of"
    },
    "@type": "Zone",
    "@id": "Zone:01",
    "inBuilding": {
        "@type": "Relationship",
        "@value": "Building:01"
    },
    "inFloor": {
        "@type": "Relationship",
        "@value": "Floor:01"
    },
    "inRoom": {
        "@type": "Relationship",
        "@value": [
            "Room:01",
            "Room:02"
        ]
    },
    "containOf": {
        "@type": "Relationship",
        "@value": [
            "Zone:02",
            "Zone:03"
        ]
    }
}

```

* Output or the annotation result: OWL (XML) 
```xml
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
  xmlns:ns1="file:///home/amirhossein/Documents/GitHub/siseg_python/"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:ns2="https://sargon-n5geh.netlify.app/ontology/1.0/classes/"
>
  <ns1:Zone rdf:about="file:///home/amirhossein/Documents/GitHub/siseg_python/Zone:01">
    <ns2:Room>Building:01</ns2:Room>
    <ns2:Zone>Floor:01</ns2:Zone>
    <ns2:Zone>['Room:01', 'Room:02']</ns2:Zone>
    <ns2:Zone>['Zone:02', 'Zone:03']</ns2:Zone>
  </ns1:Zone>
</rdf:RDF>
```

* Output or the annotation result: Turtle (RDF graph)
```text
@prefix ns1: <https://sargon-n5geh.netlify.app/ontology/1.0/classes/> .

<file:///home/amirhossein/Documents/GitHub/siseg_python/Zone:01> a <file:///home/amirhossein/Documents/GitHub/siseg_python/Zone> ;
    ns1:Room "Building:01" ;
    ns1:Zone "Floor:01",
        "['Room:01', 'Room:02']",
        "['Zone:02', 'Zone:03']" .

```

***

#### Example 2 :
* Raw data with XML format (input):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<device>
   <hasSensor>
      <type>Relationship</type>
      <value>
         <element>Sensor:01</element>
         <element>Sensor:02</element>
      </value>
   </hasSensor>
   <id>Actuator</id>
   <listening>
      <type>Relationship</type>
      <value>true</value>
   </listening>
   <locatedIn>
      <type>Relationship</type>
      <value>
         <element>Building:01</element>
         <element>Zone:02</element>
      </value>
   </locatedIn>
   <readablename>
      <type>Relationship</type>
      <value>Actuator number 01</value>
   </readablename>
   <samplerate>
      <type>Relationship</type>
      <value>45</value>
   </samplerate>
</device>

```
* Output or the annotation result (JSON-LD)
```json
{
    "@context": {
        "device": "https://w3id.org/saref#Device",
        "hassensor": "https://w3id.org/saref#SmokeSensor",
        "listening": "https://sargon-n5geh.netlify.app/ontology/1.0/data_properties/listening",
        "locatedin": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Controller",
        "readablename": "https://w3id.org/saref#Actuator",
        "samplerate": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Controller"
    },
    "@id": "hasSensor",
    "@type": "https://w3id.org/saref#SmokeSensor",
    "device": {
        "hassensor": {
            "@type": "Relationship",
            "@value": {
                "element": [
                    "Sensor:01",
                    "Sensor:02"
                ]
            }
        },
        "@id": "Actuator",
        "listening": {
            "@type": "Relationship",
            "@value": "true"
        },
        "locatedin": {
            "@type": "Relationship",
            "@value": {
                "element": [
                    "Building:01",
                    "Zone:02"
                ]
            }
        },
        "readablename": {
            "@type": "Relationship",
            "@value": "Actuator number 01"
        },
        "samplerate": {
            "@type": "Relationship",
            "@value": "45"
        },
        "@type": "https://w3id.org/saref#Device"
    }
}

```

* Output or the annotation result: OWL (XML) 
```xml
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
  xmlns:ns1="https://sargon-n5geh.netlify.app/ontology/1.0/classes/"
  xmlns:ns2="https://sargon-n5geh.netlify.app/ontology/1.0/data_properties/"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:ns3="https://w3id.org/saref#"
>
  <ns3:SmokeSensor rdf:about="file:///home/amirhossein/Documents/GitHub/siseg_python/hasSensor">
    <ns3:Device>
      <ns3:Device rdf:about="file:///home/amirhossein/Documents/GitHub/siseg_python/Actuator">
        <ns3:SmokeSensor>{'element': ['Sensor:01', 'Sensor:02']}</ns3:SmokeSensor>
        <ns2:listening>true</ns2:listening>
        <ns1:Controller>{'element': ['Building:01', 'Zone:02']}</ns1:Controller>
        <ns1:Controller>45</ns1:Controller>
        <ns3:Actuator>Actuator number 01</ns3:Actuator>
      </ns3:Device>
    </ns3:Device>
  </ns3:SmokeSensor>
</rdf:RDF>
```

* Output or the annotation result: Turtle (RDF graph)
```text
@prefix ns1: <https://sargon-n5geh.netlify.app/ontology/1.0/classes/> .
@prefix ns2: <https://w3id.org/saref#> .
@prefix ns3: <https://sargon-n5geh.netlify.app/ontology/1.0/data_properties/> .

<file:///home/amirhossein/Documents/GitHub/siseg_python/hasSensor> a ns2:SmokeSensor ;
    ns2:Device <file:///home/amirhossein/Documents/GitHub/siseg_python/Actuator> .

<file:///home/amirhossein/Documents/GitHub/siseg_python/Actuator> a ns2:Device ;
    ns1:Controller "45",
        "{'element': ['Building:01', 'Zone:02']}" ;
    ns3:listening "true" ;
    ns2:Actuator "Actuator number 01" ;
    ns2:SmokeSensor "{'element': ['Sensor:01', 'Sensor:02']}" .


```

***

#### Example 3 :
* Raw data with CSV format (input):

device     |ts                              |UL1m            |UL1a             |UL1f            |IL1m             |IL1a             |IL1f            |UL2m            |UL2a             |UL2f            |IL2m             |IL2a             |IL2f            |UL3m            |UL3a            |UL3f            |IL3m             |IL3a            |IL3f            |
|-----------|--------------------------------|----------------|-----------------|----------------|-----------------|-----------------|----------------|----------------|-----------------|----------------|-----------------|-----------------|----------------|----------------|----------------|----------------|-----------------|----------------|----------------|
|pmu_avacon1|2021-11-17T14:23:19.999921+00:00|225.656173706055|-1.38120055198669|49.9854888916016|0.909491896629334|-1.52175891399384|49.9832382202149|226.996444702148|0.721798896789551|49.9851837158203|0.798067927360535|0.625345230102539|49.9879722595215|225.658065795898|2.8104932308197 |49.9852333068848|0.842253506183624|2.70594334602356|49.9860916137695|

* Output or the annotation result (JSON-LD)
    * Each row in CSV file corresponds to a pair with json object as the value of the pair in the resulting json ld output. 
```json
{
    "@context": {
        "device": "https://w3id.org/saref#Device",
        "UL1m": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute",
        "has_channel": "https://sargon-n5geh.netlify.app/ontology/1.0/object_properties/has_channel",
        "UL1a": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle",
        "UL1f": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency",
        "IL1m": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute",
        "IL1a": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle",
        "IL1f": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency",
        "UL2m": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute",
        "UL2a": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle",
        "UL2f": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency",
        "IL2m": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute",
        "IL2a": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle",
        "IL2f": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency",
        "UL3m": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute",
        "UL3a": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle",
        "UL3f": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency",
        "IL3m": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute",
        "IL3a": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle",
        "IL3f": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency"
    },
    "@id": "pmu_avacon1",
    "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/PMU",
    "device": {
        "@id": "device",
        "@value": "pmu_avacon1",
        "@type": "https://w3id.org/saref#Device"
    },
    "ts": "2021-11-17T14:23:19.999921+00:00",
    "has_channel": {
        "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/object_properties/has_channel",
        "UL1m": {
            "@id": "UL1m",
            "@value": 225.656173706055,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute"
        },
        "UL1a": {
            "@id": "UL1a",
            "@value": -1.38120055198669,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle"
        },
        "UL1f": {
            "@id": "UL1f",
            "@value": 49.9854888916016,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency"
        },
        "IL1m": {
            "@id": "IL1m",
            "@value": 0.909491896629334,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute"
        },
        "IL1a": {
            "@id": "IL1a",
            "@value": -1.52175891399384,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle"
        },
        "IL1f": {
            "@id": "IL1f",
            "@value": 49.9832382202149,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency"
        },
        "UL2m": {
            "@id": "UL2m",
            "@value": 226.996444702148,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute"
        },
        "UL2a": {
            "@id": "UL2a",
            "@value": 0.721798896789551,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle"
        },
        "UL2f": {
            "@id": "UL2f",
            "@value": 49.9851837158203,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency"
        },
        "IL2m": {
            "@id": "IL2m",
            "@value": 0.798067927360535,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute"
        },
        "IL2a": {
            "@id": "IL2a",
            "@value": 0.625345230102539,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle"
        },
        "IL2f": {
            "@id": "IL2f",
            "@value": 49.9879722595215,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency"
        },
        "UL3m": {
            "@id": "UL3m",
            "@value": 225.658065795898,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute"
        },
        "UL3a": {
            "@id": "UL3a",
            "@value": 2.8104932308197,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle"
        },
        "UL3f": {
            "@id": "UL3f",
            "@value": 49.9852333068848,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency"
        },
        "IL3m": {
            "@id": "IL3m",
            "@value": 0.842253506183624,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute"
        },
        "IL3a": {
            "@id": "IL3a",
            "@value": 2.70594334602356,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle"
        },
        "IL3f": {
            "@id": "IL3f",
            "@value": 49.9860916137695,
            "@type": "https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency"
        }
    }
}

```

* Output or the annotation result: OWL (XML) 
```xml
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF
  xmlns:ns1="https://sargon-n5geh.netlify.app/ontology/1.0/classes/"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:ns2="https://sargon-n5geh.netlify.app/ontology/1.0/object_properties/"
  xmlns:ns3="https://w3id.org/saref#"
>
  <ns1:PMU rdf:about="file:///home/amirhossein/Documents/GitHub/siseg_python/pmu_avacon1">
    <ns3:Device rdf:datatype="https://w3id.org/saref#Device">pmu_avacon1</ns3:Device>
    <ns2:has_channel>
      <ns2:has_channel rdf:nodeID="N3fc62b42bcdc46e1923f3a6cfccb147a">
        <ns1:Maqnitute rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute">225.656173706055</ns1:Maqnitute>
        <ns1:Maqnitute rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute">0.909491896629334</ns1:Maqnitute>
        <ns1:Maqnitute rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute">226.996444702148</ns1:Maqnitute>
        <ns1:Maqnitute rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute">0.798067927360535</ns1:Maqnitute>
        <ns1:Maqnitute rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute">225.658065795898</ns1:Maqnitute>
        <ns1:Maqnitute rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute">0.842253506183624</ns1:Maqnitute>
        <ns1:Angle rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle">-1.38120055198669</ns1:Angle>
        <ns1:Angle rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle">-1.52175891399384</ns1:Angle>
        <ns1:Angle rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle">0.721798896789551</ns1:Angle>
        <ns1:Angle rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle">0.625345230102539</ns1:Angle>
        <ns1:Angle rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle">2.8104932308197</ns1:Angle>
        <ns1:Angle rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle">2.70594334602356</ns1:Angle>
        <ns1:Frequency rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency">49.9854888916016</ns1:Frequency>
        <ns1:Frequency rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency">49.9832382202149</ns1:Frequency>
        <ns1:Frequency rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency">49.9851837158203</ns1:Frequency>
        <ns1:Frequency rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency">49.9879722595215</ns1:Frequency>
        <ns1:Frequency rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency">49.9852333068848</ns1:Frequency>
        <ns1:Frequency rdf:datatype="https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency">49.9860916137695</ns1:Frequency>
      </ns2:has_channel>
    </ns2:has_channel>
  </ns1:PMU>
</rdf:RDF>
```

* Output or the annotation result: Turtle (RDF graph)
```text
@prefix ns1: <https://sargon-n5geh.netlify.app/ontology/1.0/classes/> .
@prefix ns2: <https://w3id.org/saref#> .
@prefix ns3: <https://sargon-n5geh.netlify.app/ontology/1.0/object_properties/> .

<file:///home/amirhossein/Documents/GitHub/siseg_python/pmu_avacon1> a ns1:PMU ;
    ns3:has_channel [ a ns3:has_channel ;
            ns1:Angle "-1.52175891399384"^^ns1:Angle,
                "-1.38120055198669"^^ns1:Angle,
                "0.625345230102539"^^ns1:Angle,
                "0.721798896789551"^^ns1:Angle,
                "2.70594334602356"^^ns1:Angle,
                "2.8104932308197"^^ns1:Angle ;
            ns1:Frequency "49.9832382202149"^^ns1:Frequency,
                "49.9851837158203"^^ns1:Frequency,
                "49.9852333068848"^^ns1:Frequency,
                "49.9854888916016"^^ns1:Frequency,
                "49.9860916137695"^^ns1:Frequency,
                "49.9879722595215"^^ns1:Frequency ;
            ns1:Maqnitute "0.798067927360535"^^ns1:Maqnitute,
                "0.842253506183624"^^ns1:Maqnitute,
                "0.909491896629334"^^ns1:Maqnitute,
                "225.656173706055"^^ns1:Maqnitute,
                "225.658065795898"^^ns1:Maqnitute,
                "226.996444702148"^^ns1:Maqnitute ] ;
    ns2:Device "pmu_avacon1"^^ns2:Device .


```
