# BSpell: Bangla Spelling Correction

## Citation
If you use the BSpell tool or dataset in your research, please cite the following paper:

**Paper Title:** *BSpell: A CNN-Blended BERT Based Bangla Spell Checker*

## Installation Options
- **Using "BSpell_Env.yml":** You can create the virtual environment easily with the provided .yml file.
    - Command: `conda env create -f BSpell_Env.yml`
- **Using "requirements.txt":** If the .yml file doesn't work, you can use the "requirements.txt" file and "pip" to install dependencies. After creating a basic virtual environment, use this command to install all the packages:
    - Command: `pip install -r requirements.txt`

# Running BSpell for Bangla Spelling Correction
To run BSpell for Bangla spelling correction, please follow the steps below:

    ## Prerequisites
    Ensure that you have set up the necessary environment and have the required files:

    - **Model File:** You should have the saved model file for BSpell.
    - **Tokenizer:** The tokenizer used by BSpell for processing text.
    - **Dictionary of Index-Top Words:** The dataset for mapping indices to top words.

    ## Command for Run Correcting Bangla Text
    Use the following command to correct error-prone Bangla text:
    - Run the "main.py" file:
        - Command : python main.py input_file output_file tokenizer_path dict_Of_index_Top_Words_path model_path
        - Here 
            * input_file: Path to the input file containing error-prone Bengali text.
            * output_file: Path to the output file for the corrected text.
            * tokenizer_path: Path to the tokenizer file.
            * dict_Of_index_Top_Words_path: Path to the dictionary of index-top words file.
            * model_path: Path to the saved BSpell model.

# Model and Dataset Link:
Drive Link: https://drive.google.com/drive/folders/1bMKEVNwBef84TFl-Z5tSRBtIZmooYCUm?usp=sharing
