import os
import json
import base64
import requests
import jsonlines
from multiprocessing import Pool
from openai import OpenAI
from functools import partial
import time
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')



client = OpenAI(
    base_url=xx,
    api_key=xx,
)





task = """Assume that you are a mature physicist,I need you to rate the input image according to the following scoring criteria and give the score first and explain later. Please only focus on the differences between the picture and the normal physical phenomenon, and ignore the style of the picture and the unimportant parts that are not the subject. Now, I will give you an image. Don‘t be strict with your grading.\n"""
answer = """Please answer in the format {'scene_score': Integer value from 0 to 2, 'phy_score': Integer value from 0 to 3, 'scene_reason': ,'phy_reason': }. Pay special attention to the physical laws, and be lenient in scoring the scene.\n"""

output_dict = {}

def process_data(data_tmp):
    # print(data_tmp['law'])
    scene = data_tmp['scene']
    normal = data_tmp['normal']
    grading = data_tmp['grading']
    dalle3_path = data_tmp['DALLE3']
    img_path = dalle3_path
    
    try:  
        if os.path.exists(img_path):
            prompt = f"""Scene: {scene}\nNormal physical phenomenon: {normal}\nDetailed Scoring Criteria:{grading}\n """ + extra
            content = task + prompt + answer
            try:
                base64_image = encode_image(img_path)
            except:
                print('encode image error!!')
            # print(base64_image)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": content},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                # response_format={"type": "json_object"},
                max_tokens=500,
            )
            print(response.choices[0].message.content)
            score = response.choices[0].message.content
        else:
            print('no image')
            score = 'no image'
        
    except:
        print('error')
        score = 'error'

    time.sleep(1)
    data_tmp[f'{model}_score'] = score




    return data_tmp


def main():
    input_file_path = 'xx'
    output_file_path = 'xx_eval.json'

    with open(input_file_path, 'r') as f:
        data = json.load(f)

    pool = Pool(processes=12)  # Adjust the number of processes as per your machine's capability
    result = pool.map(process_data, data)

    with open(output_file_path, 'w') as f:
        json.dump(result, f)

if __name__ == '__main__':
    main()
