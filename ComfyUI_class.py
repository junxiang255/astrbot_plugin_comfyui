import requests
import json
import time
import uuid
import random
from typing import Dict, Any, Optional
class ComfyUIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:6006/"):
        self.base_url = base_url.rstrip("/")
        self.client_id = str(uuid.uuid4())

    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统状态"""
        response = requests.get(f"{self.base_url}/system_stats")
        print(self.base_url)
        # print(response.json())
        system_stats=response.json()
        print("系统是:",system_stats["system"]["os"])
        print("显卡是:",system_stats["devices"][0]["name"])
        return response.json()
    def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态"""
        response = requests.get(f"{self.base_url}/queue")
        queue=response.json()
        print(queue)
        return response.json()
    def submit_workflow(self,workflow: Dict[str, Any]) -> str:
        """提交工作流"""
        payload = {
            "prompt": workflow,
            "client_id": self.client_id
        }
        response = requests.post(f"{self.base_url}/prompt", json=payload)
        result = response.json()
        return result["prompt_id"]

    def get_history(self, prompt_id: Optional[str] = None) -> Dict[str, Any]:

        if prompt_id:
            response = requests.get(f"{self.base_url}/history/{prompt_id}")
        else:
            response = requests.get(f"{self.base_url}/history")
        return response.json()

    def upload_image(self, image_path: str) -> Dict[str, Any]:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {'overwrite': 'true'}
            response = requests.post(
                f"{self.base_url}/upload/image",
                files=files,
                data=data
            )
        return response.json()
    def download_image(self, filename: str, subfolder: str = "",
                      image_type: str = "output") -> bytes:

        params = {
            'filename': filename,
            'subfolder': subfolder,
            'type': image_type
        }
        response = requests.get(f"{self.base_url}/view", params=params)
        return response.content

    def wait_for_completion(self, prompt_id: str, timeout: int = 300) -> Dict[str, Any]:
        start_time = time.time()

        while time.time() - start_time < timeout:
            history = self.get_history(prompt_id)
            # print(history)

            if prompt_id in history:
                status = history[prompt_id]["status"]["status_str"]
                print(status)
                # print(history[prompt_id])
                if status in ["success", "error"]:

                    return history[prompt_id]


            time.sleep(1)
        raise TimeoutError(f"任务{prompt_id}未能在{timeout}秒内完成")

    def cancel_task(self, prompt_id: str) -> bool:
        """取消任务"""
        payload = {"delete": [prompt_id]}
        response = requests.post(f"{self.base_url}/queue", json=payload)
        return response.status_code == 200
class WorkflowBuilder:
    def __init__(self):
        self.workflow={}
        self.node_counter=1
    def add_checkpoint_loader(self,ckpt_name) -> int:
        node_id = self.node_counter
        self.workflow[str(node_id)]={
            "inputs": { "ckpt_name":ckpt_name },
            "class_type":"CheckpointLoaderSimple",
            "_meta": {
                "title": "Checkpoint加载器（简易）"
            }
        }
        self.node_counter += 1
        return node_id
    def add_lord_1(self,lora_name:str,strength_model:float,strength_clip=float)-> int:
        node_id = self.node_counter
        self.workflow[str(node_id)]={
            "inputs": { "lora_name":lora_name,
            "strength_model":strength_model,
            "strength_clip": strength_clip,
            "model":["1",0],
            "clip":["1",1]
            },
            "class_type": "LoraLoader",
            "_meta": {
                "title": "画风LoRA"}
        }

        self.node_counter += 1
        return node_id
    def add_load_2(self,lora_name:str,strength_model:float,strength_clip=float)-> int:
        node_id = self.node_counter
        self.workflow[str(node_id)]={
            "inputs": { "lora_name":lora_name,
            "strength_model":strength_model,
            "strength_clip": strength_clip,
            "model":["2",0],
            "clip":["2",1]
            },
            "class_type": "LoraLoader",
            "_meta": {
            "title": "人物LoRA"
            }
        }
        self.node_counter += 1
        return node_id
    def add_load_3(self,lora_name:str,strength_model:float,strength_clip=float)-> int:
        node_id = self.node_counter
        self.workflow[str(node_id)]={
            "inputs": { "lora_name":lora_name,
            "strength_model":strength_model,
            "strength_clip": strength_clip,
            "model":["3",0],
            "clip":["3",1]
            },
            "class_type": "LoraLoader",
            "_meta": {
            "title": "眼睛LoRA"
            }
        }
        self.node_counter += 1
        return node_id
    def add_load_4(self,lora_name:str,strength_model:float,strength_clip=float)-> int:
        node_id = self.node_counter
        self.workflow[str(node_id)]={
            "inputs": { "lora_name":lora_name,
            "strength_model":strength_model,
            "strength_clip": strength_clip,
            "model":["4",0],
            "clip":["4",1]
            },
            "class_type": "LoraLoader",
            "_meta": {
            "title": "手部LoRA"
            }
        }
        self.node_counter += 1
        return node_id
    def add_load_5(self,lora_name:str,strength_model:float,strength_clip=float)-> int:
        node_id = self.node_counter
        self.workflow[str(node_id)]={
            "inputs": { "lora_name":lora_name,
            "strength_model":strength_model,
            "strength_clip": strength_clip,
            "model":["5",0],
            "clip":["5",1]
            },
            "class_type": "LoraLoader",
            "_meta": {
            "title": "衣服LoRA"
            }
        }
        self.node_counter += 1
        return node_id
    def add_load_6(self,lora_name:str,strength_model:float,strength_clip=float)-> int:
        node_id = self.node_counter
        self.workflow[str(node_id)]={
            "inputs": { "lora_name":lora_name,
            "strength_model":strength_model,
            "strength_clip": strength_clip,
            "model":["6",0],
            "clip":["6",1]
            },
            "class_type": "LoraLoader",
            "_meta": {
            "title": "色色LoRA"
            }
        }
        self.node_counter += 1
        return node_id
    def add_ksampler(self) -> int:
        seed=random.randint(1, 999999999999999)
        print(seed)
        node_id=self.node_counter
        self.workflow[str(node_id)]={
            "inputs": {
                "seed": seed ,
                "steps": 27,
                "cfg": 5.7,
                "sampler_name": "euler_ancestral",
                "scheduler": "karras",
                "denoise": 0.8,
                "model": ["7",0],
                "positive": ["9",0],
                "negative": ["10",0],
                "latent_image": ["11",0]
            },
            "class_type": "KSampler",
            "_meta": {
            "title": "K采样器"}

        }
        self.node_counter += 1
        return node_id

    def add_text_encoder(self,text:str,)-> int:
        node_id = self.node_counter
        self.workflow[str(node_id)]={
            "inputs": {
                "text": text,
                "clip":["7", 1]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "正向提示词"
            }
        }

        self.node_counter += 1
        return node_id
    def add_Negative_text_encoder(self,text:str)-> int:
        node_id = self.node_counter
        self.workflow[str(node_id)] = {
            "inputs": {
                "text": text,
                "clip": ["7", 1]

            },
            "class_type": "CLIPTextEncode",
            "_meta": {
                "title": "负面提示词"
            }
        }
        self.node_counter += 1
        return node_id
    def add_Latent(self,width:int,height:int,batch_size:int)-> int:
        node_id=self.node_counter
        self.workflow[str(node_id)] = {
            "inputs": {
                "width": width,
                "height": height,
                "batch_size":batch_size,
            },
            "class_type": "EmptyLatentImage",
            "_meta": {
            "title": "空Latent图像"}
        }
        self.node_counter += 1
        return node_id
    def add_vae_decode(self) -> int:
        node_id = self.node_counter
        self.workflow[str(node_id)] = {
            "inputs": {
                "samples": ["8",0],
                "vae": ["1", 2]
            },
            "class_type": "VAEDecode",
            "_meta": {
            "title": "VAE解码"
            }
        }
        self.node_counter += 1
        return node_id

    def add_save_image(self) -> int:
        node_id = self.node_counter
        self.workflow[str(node_id)] = {
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": ["12", 0]
            },
            "class_type": "SaveImage",
            "_meta": {
            "title": "保存图像"
            }
        }
        self.node_counter += 1
        return node_id

    def build(self) -> Dict[str, Any]:

        return self.workflow
