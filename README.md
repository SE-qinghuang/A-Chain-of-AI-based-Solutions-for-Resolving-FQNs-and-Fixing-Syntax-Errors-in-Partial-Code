# A-Chain-of-AI-based-Solutions-for-Resolving-FQNs-and-Fixing-Syntax-Errors-in-Partial-Code

### The directory structure of the project is as follows
```
├─Experimental Results
│  ├─Prompt
│  │      Prompt_For_Java_Code_Fix.txt
│  │      Prompt_For_Java_Compile.txt
│  │      Prompt_For_Java_CoT.txt
│  │      Prompt_For_Java_Direct.txt
│  │      Prompt_For_Java_Error_Message_Enhance.txt
│  │      Prompt_For_Java_Simplename_Extraction.txt
│  │      Prompt_For_Java_Simplename_to_FQN.txt
│  │      Prompt_For_Python_Code_Fix.txt
│  │      Prompt_For_Python_CoT.txt
│  │      Prompt_For_Python_Direct.txt
│  │      Prompt_For_Python_Error_Message_Enhance.txt
│  │
│  ├─RQ1
│  │      Result_For_RQ1.csv
│  │
│  ├─RQ2
│  │  ├─Java
│  │  │      PCR-Chain_For_Java.py
│  │  │      Result_For_RQ2_PCR-Chain_Java.csv
│  │  │
│  │  └─Python not done
│  │          PCR-Chain_For_Python.py
│  │          Result_For_RQ2_PCR-Chain_Python.csv
│  │
│  ├─RQ3
│  │  ├─Java
│  │  │      Result_For_RQ3_PCR-CoT_Java.csv
│  │  │      Result_For_RQ3_PCR-D_Java.csv
│  │  │      Result_For_RQ3_PCR-withoutEME_Java.csv
│  │  │
│  │  └─Python
│  │          Result_For_RQ3_PCR-CoT_Python.csv
│  │          Result_For_RQ3_PCR-D_Python.csv
│  │          Result_For_RQ3_PCR-withoutEME_Python.csv
│  │
│  └─RQ4
│      ├─Content_representation
│      │      Content_representation.py
│      │      Result_For_RQ4_Content_representation.csv
│      │
│      ├─Demonstration_example
│      │      Demonstration_example.py
│      │      Result_For_RQ4_Demonstration_example_dissimilar_first.csv
│      │      Result_For_RQ4_Demonstration_example_similar_first.csv
│      │
│      └─Instruction
│              Instruction.py
│              Result_For_RQ4_without_Instruction.csv
│
└─Experiments Setup
        Java_Dataset.csv
        Python_Dataset.csv
 ```
