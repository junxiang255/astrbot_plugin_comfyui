from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from ComfyUI_class import ComfyUIClient, WorkflowBuilder
@register("ComfyUI_qqbot", "junxiang255", "一个简单的ComfyUIapi_sdxl插件", "1.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 sdxl。注册成功后，发送 `/asxl` 就会触发这个指令
    @filter.command("sdxl")
    async def qqbot_ComfyUI(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        client = ComfyUIClient("http://127.0.0.1:6006")
        builder = WorkflowBuilder()
        builder = WorkflowBuilder()
        builder.add_checkpoint_loader("waiIllustriousSDXL_v160.safetensors")
        builder.add_lord_1("Yuzu Soft[style]-Illus.safetensors", 0, 0)
        builder.add_load_2("Miyako_Kujo_2b_WAIillu-000026.safetensors", 1.4, 1)
        builder.add_load_3("2725219?type=Model&format.safetensors", 0.4, 1)
        builder.add_load_4("2655999?type=Model&format.safetensors", 0.4, 1)
        builder.add_load_5("high-low-wedding-dress-illustriousxl-lora-nochekaiser.safetensors", 0.4, 1)
        builder.add_load_6("Caught NTR-Sex-IL_NAI_PY.safetensors", 0, 0)
        builder.add_ksampler()
        builder.add_text_encoder(event.message_str)
        builder.add_Negative_text_encoder(
            "censored,mosaic censoring,bar censor,signature,username,logo,bad hands,mutated hands,watermark,missing limb,missing finger,")
        builder.add_Latent(1024, 1600, 1)
        builder.add_vae_decode()
        builder.add_save_image()
        builder.build()
        workflow = builder.build()
        print(workflow)
        prompt_id = client.submit_workflow(workflow)
        yield event.plain_result(f"任务已提交，ID: {prompt_id}")
        result = client.wait_for_completion(prompt_id)
        print(result["status"])
        node_id =builder.add_save_image() - 1
        print(node_id)
        if result["status"]["status_str"] == "success":
            outputs = result["outputs"]


            output = outputs[f"{node_id}"]["images"]
            for image_info in output:
                print(output)
                filename = image_info["filename"]
                image_data = client.download_image(filename)

                with open(f"data\plugins/astrbot_plugin_comfyui/tp/generated_{filename}", "wb") as f:
                    f.write(image_data)
                    yield event.plain_result(f"图片已生成并保存为 generated_{filename}")
                    yield event.image_result(f"data\plugins/astrbot_plugin_comfyui/tp/generated_{filename}")
                
                
            
               
         

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
