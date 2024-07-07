import base64
import json
import os
from multiprocessing import Pool
import requests
from openai import OpenAI


API_KEY = xx
API_ENDPOINT = xx



def process_data(data_tmp):
    client = OpenAI(
    base_url=API_ENDPOINT,
    api_key=API_KEY,
    )

    task = """Assume that you are a mature physicist. I need you to generate detailed scoring criteria based on my requirements and the input pictures, as to whether the pictures correctly reflect the laws of physics. Please only focus on the differences between the picture and the normal physical phenomenon, and ignore the style of the picture and the unimportant parts that are not the subject. Then I need you to accurately score the input pictures based on the scoring criteria you generated. \n"""

    template = """
    Scene Score:
    0 point: All of the required scene is incorrect, whether or not the laws of physics are correct.
    1 point: Some of the required scene are partially incorrect, whether or not the laws of physics are correct.
    2 points: The picture accurately reflects the required scene, whether or not the laws of physics are correct.
    Physical laws Score:
    0 point: The representation of the physical law is completely incorrect.
    1-2 point: The representation of the physical law is partially incorrect. Scores decrease based on the degree of error.
    3 point: The picture correctly reflects the laws of physics.\n
    """

    answer = """Please just answer the detailed scoring criteria with nothing alse."""

    normal = data_tmp['normal']
    scene = data_tmp['scene']

    prompt = f"""Scene: {scene}\nPhysical laws: {normal}\n"""

    content = task + prompt + template + answer

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": content},
                    ],
                }
            ],
            max_tokens=2000,
        )
        print(response.choices[0].message.content[:10])
        grading = response.choices[0].message.content
        
    except Exception as e:
        grading = str(e)

    data_tmp['grading'] = grading
    return data_tmp

def main():
    input_file_path = './phy_chem_eval_all.json'
    output_file_path = './phy_chem_eval_all_grading.json'

    with open(input_file_path, 'r') as f:
        data = json.load(f)

    pool = Pool(processes=12)  # Adjust the number of processes as per your machine's capability
    result = pool.map(process_data, data)

    with open(output_file_path, 'w') as f:
        json.dump(result, f)

if __name__ == '__main__':
    main()
