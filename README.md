# Anguix Command Line Version
This software aggregates Sabio-RK information to a pre-existent Neo4J Reactome Graph Database.

# Before you Start!

- Before use this software, please install **Neo4J Desktop** version and add the latest version of **Reactome Graph Database**, according their instructions.
- Once downloaded, create a folder called "**.env**" in the project main folder. This will contain your local information to be able to add the new nodes.
- Before using the software, open Neo4J Desktop and run the **Reactome Graph Database**, after this, you're ready to use **Anguix Command Line Version**.

# .env File Model

scheme = "neo4j" <br>
host_name = "localhost" <br>
database = **Your Database Name** <br>
port = **Your Port** <br>
user = **Your Username** <br>
password = **Your Password** <br>
<br>

# Running the Software:

- Once started, the software will check for dependencies and display basic information about both Sabio-RK and Reactome.
- The software will ask if you want to operate in **Auto** or **Manual** mode:

# Auto Mode:

The auto mode will seek for all organisms in common for both Sabio-RK and Reactome, and will add them to the graph. Due to Sabio-RK server timeout, this mode tends to be very time consuming.

# Manual Mode:

Adds only available reactions from a single desired organism. The list will be displayed to the user.

# The Outcome

If everything works fine, the reactions will be displayed on the Reactome Graph Database, and you will be able to use it as you wish.

## <p align="center">Acessing Anguix Newly Added Information</p> 

After the completion of all tasks, you will be able to access all the information you gathered into
Reactome Graph Database.

- Open your updated graph on Neo4J.

### Query 1 - If you want to check if all reactions were added, you can run the following:

```
// SELECT ALL SABIO-RK REACTIONS
MATCH (n:SabioRkReaction)-[:kineticDataFor]-(k),
(n)-[:generalReactionFor]-(r), (k)-[:parameterInfo]-> (p)
RETURN n, k, r, p
```

### Query 2 - If you want to know what pathways has more Sabio-RK Kinetic data inserted:

```
// SELECT PATHWAY THAT HAS MORE SABIO-RK KINETICS
MATCH (p:Pathway)-[n]-(r:Reaction),
(x:SabioRkReaction)-[:generalReactionFor]-(r)
WITH p, COUNT(*) AS num ORDER BY num DESC
RETURN num, p.displayName
```

### Query 3 - If you want to choose a specific Sabio-RK reaction and find its related nodes:

```
// SELECT SABIO-RK REACTION BY ID NUMBER EXAMPLE
MATCH (n:SabioRkReaction{SabioReactionID: 594})-[:kineticDataFor]-(k),
(n)-[:generalReactionFor]-(r)
RETURN n, k, r
```

### Query 4 - If you want to find all nodes from a Reactome Pathway, including newly added corresponding Sabio-RK Reaction nodes:

```
// ANGUIX GRAPH DATABASE REACTIONS
MATCH (p:Pathway)-[:hasEvent]-(r:Reaction),
(x:SabioRkReaction)-[:generalReactionFor]-(r),
(p:Pathway)-[:hasEvent]-(z:Reaction)
WHERE p.displayName = ”Gluconeogenesis” AND
p.speciesName = ”Homo sapiens”
RETURN r, x, z
```

### Query 5 - If you Regreted Using Anguix and Desire to Remove All Added Information:


```
// ERASE ANGUIX
MATCH (n:SabioRkReaction)-[:kineticDataFor]-(k), (n)-[:generalReactionFor]-(r), 
(k)-[:parameterInfo]->(p)
DETACH DELETE n, k, p
```

## <p align="center">Adittional Information</p>

### Modelling and Sabio-RK kinetic information insertion on Reactome Graph Database:

Under the same Sabio-RK Entry ID, what would be a single reaction, there is multiple publications that might be associated. Because of that,
node derivations is a must. Besides that, there is several parameters that can be considered general information for all the reactions (**Global parameters**) and other that can be directly related to the reaction participants (**Parameters associated with specific chemical species**).

- **Global parameters**:

  - kcat
  - Keq
  - kinact
  - pH
  - pKa 
  - Rate Const.
  - Specific Enz. Activity
  - Time
  - Volume
  - Vmax

- **Parameters associated with specific chemical species**:

  - Activation Constant
  - Concentration
  - EC50
  - IC50
  - Hill coefficient
  - Hill constant
  - kcat/S half
  - kcat/Km
  - Kd
  - Ki
  - Km
  - S half
  - unknown*
  - Vmax/Km
  
  The data lists as **unknown** are not clearly explained on <a href="http://sabio.h-its.org/layouts/content/documentation.gsp">Sabio-RK documentation</a>, however, several times this information is associated with chemical species. For these purposes we consider **unknown** as just another parameter. <br>
  Inside an unique identifier, it can be obtain a variation of: catalyst, mutation or not, publication, and many others. Besides that parameters such
as **kcat**, **km** etc., varies through different experimental conditions and can’t be disposed in the same node. Because of that, we developed a way to display the information without causing disturbances on the previous database schema as can be seen below in **Anguix Schema Figure**:

<p align="center">
  <img width="700" height="700" src="https://user-images.githubusercontent.com/81723337/175721383-fe9086ed-a50b-49f2-bf4c-b146bd04044d.jpg">
</p>

In **Anguix Schema Figure A** , it is possible to observe how the relationship between the reactions already existing in the graph with the reactions of Sabio-RK is established, where n reactions of Reactome can be related to n reactions of Sabio-RK, and each of these, in turn, has a 1 to n relationship with its derivations, and these will eventually again branch through its parameters. <br>
In **Anguix Schema Figure B**, it can be seen a visual example of how this relationship occurs and its cardinality. And finally, in **Anguix Schema Figure C**, an overview of how this new information is arranged in the new database. Next, we list all the properties of nodes Sabio-RK Information, Derived Kinetic Data and finally Kinetic Data Parameters:

- **Sabio-RK Information Node attributes**:
  - Authored
  - Sabio Reaction ID
  - Entry ID
  - Enzyme Name
  - Ec. Number
  - Kegg Reaction ID
  - Pathway
  - Product
  - Reaction Equation
  - Reactome Reaction ID
  
- **Derived Kinetic Data attributes**:

  - Authored
  - Derived Entry
  - Activator
  - Buffer
  - Cellular Location
  - Cofactor
  - Enzyme Variant
  - Inhibitor
  - Kinetic Mechanism
  - Other Modifier
  - Ph
  - Rate Equation
  - Temperature
  - Tissue
  - UniprotID
  - Publication
  - Pubmed ID
 
- **Kinetic Data Parameters attributes**:
 
  - Parameter Type/ Name
  - Parameter Associated Species
  - Parameter Start Value
  - Parameter End Value
  - Parameter Standard Deviation
  - Parameter Unit
  
  The biggest motivation for having a second derivation with the data with the node **Kinetic Data Parameters**, is because of the variation of possible parameters, once they were placed in the class **Derived Kinetic Data**, the names of the species associated with the parameter itself, would generate
unique attribute names (such as **km [NADH]**, **Kcat [CoA]**, etc.), which could compromise the efficiency of the database in terms of searches. <br>
Some parameters may vary depending on which kinetic law the reaction was measured, however, they all work the same in the modeling aspect, and the
example above covers all cases.

## <p align="center">Anguix Python Script Description</p>

1. **Class Reactome API** : This class is responsible for making calls to Reactome API.

    - **fetch_organisms_list**: Responsible for consulting the list of current
organisms from Reactome.
    - **fetch_organism_abbreviation**: Similar to the previous method, but returns the abbreviation corresponding to the requested organism. Extremely important for later regex procedures.
    
2. **Class SabioRk API**: This class is responsible for making calls to Sabio-RK API.

    - **fetch_organisms_list**: Responsible for consulting the list of current organisms from Sabio-RK.
    - **fetch_data_from**: Fetch specific information from a given organism and save only reactions that have Reactome Reaction ID.
    - **clean data**: 1. Remove columns that do not have Reactome Reaction ID, 2. Remove abbreviations of organisms that are not part of the selected organism.

3. **Class AnguixBaseFormat**: This class is responsible for creating the base format for the subsequent transformations that Anguix needs to perform to create the nodes.

    - **fetch_organisms_list**: This method returns the list of organisms common to Reactome and Sabio-RK.
    - **work** : Searches for data in Sabio-RK.

4. **Class Node Creator**: This class is responsible for adding the information obtained in Neo4J.

    - **create_query_parent_node**: Responsible for creating the queries of the parent nodes.
    - **create_query_child_node**: Responsible for creating the queries of the child nodes.
    - **create_parameter_node**: Responsible for creating the queries of the parameter nodes.
    - **create_queries**: Completes the queries created earlier, adding the necessary commands for this and at the same time creates unique variables for each node added to avoid errors in Neo4J.
 
5. **Class Stepinfo**: This class stores the information that is relevant during all the steps that Anguix performs.

    - **init**: Stores ”steps” as objects.
    - **str** : responsible for printing the information obtained in the class to the user.

6. **Main_program_Main.py**: Allows the user to choose the operation modes of Anguix, **Manual** , where the user chooses a specific organism to add the
constants or **Auto**, where the user adds all the possible organisms, and does this using the classes previously determined to make the program
work.

7. **Dependencies**:

    - Pandas
    - Requests
    - Jinja2
    - neo4j
    - PySimpleGUI
    - tkinker
