```mermaid
flowchart TD
    A["E-Commerce Source Data"] --> B["Databricks Auto Loader"]
    B --> C["Bronze Layer - Raw Data"]
    C --> D["Silver Layer - Data Cleaning and Transformation"]
    D --> E["Gold Layer - Business Aggregations"]
    E --> F["Databricks SQL Dashboard"]

    C --> G["Delta Tables"]
    D --> G
    E --> G

    H["Unity Catalog"] -. "Data Governance" .-> G
    I["Lakeflow Spark Declarative Pipelines"] -. "Pipeline Processing" .-> C
    I -.-> D
    I -.-> E