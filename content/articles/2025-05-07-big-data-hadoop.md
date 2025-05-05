---
Title: Big Data with Hadoop
Date: 2025-05-07 07:00
Category: Machine Learning
Tags: big-data, hadoop, data-engineering
Slug: 2025-05-07-big-data-hadoop
Status: draft
---

# Introduction

# What is Apache Hadoop?

<figure>
  <pre class="mermaid">
      flowchart TB
        subgraph L1 ["Processing framework layer"]
            direction LR
            MR[MapReduce]
            SP[Spark]
        end
        subgraph L2 ["Cluster resource management layer"]
            YARN["Yet Another Resource Negotiator"]
        end
        subgraph L3 ["Distributed storage layer"]
            HDFS["Hadoop Distributed File System"]
        end
        subgraph L4 ["Disks and processors"]
            direction LR
            S1[(Server 1)]
            S2[(Server 2)]
            S3[(Server 3)]
            S4[(Server 4)]
        end
        MR --> YARN
        SP --> YARN
        YARN --> HDFS
        HDFS --> S1 & S2 & S3 & S4
  </pre>
  <figcaption style="text-align: center">Figure 1. Example of Hadoop architecture</figcaption>
</figure>
