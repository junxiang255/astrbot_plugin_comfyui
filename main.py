from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp
from astrbot.core.utils.session_waiter import (
    session_waiter,
    SessionController,
)
import sys
class_path = "data/plugins/astrbot_plugin_comfyui"
sys.path.append(rf"{class_path}")
from ComfyUI_class import ComfyUIClient, WorkflowBuilder,custom_WorkflowBuilder
from astrbot.api.message_components import *
import re
import os


"""checkpoint底模"""
checkpoint_loader= "waiIllustriousSDXL_v160.safetensors"


"""风格"""
style_1 = "Yuzu Soft[style]-Illus.safetensors"
old_list_style = [style_1]
style_name_list = ["柚子社风格"]
list_style = [f"{i}. {style}--{name}" for i, (style, name) in enumerate(zip(old_list_style,style_name_list),start=1)]
style_lord= style_1
style_lord_model_Strength = 1 
style_lord_cilp_Strength = 1

"""人物"""

character_1 = "Shirayuki_Noa_1b_nai-000010.safetensors" #白雪乃爱
character_2 ="Miyako_Kujo_2b_WAIillu-000026.safetensors"#九条都
character_3 = "Sylvia_(Kiniro)_1a_nai-000039.safetensors"#希尔维娅
character_4 = "Sumizome_Nozomi_1a_nai-000028.safetensors"#墨染希
character_5 = "Jougasaki_Ayaka_1a_nai-000047.safetensors" #城崎绚华
character_name_list = ["白雪乃爱", "九条都", "希尔维娅", "墨染希", "城崎绚华"]
old_list_character = [character_1, character_2, character_3, character_4, character_5]
list_character = [f"{i}. {character}--{name}" for i, (character, name) in enumerate(zip(old_list_character,character_name_list),start=1)]
character_lord = character_1
character_lord_model_Strength = 1.2
character_lord_cilp_Strength = 1

"""衣服"""
clothes_1 = "high-low-wedding-dress-illustriousxl-lora-nochekaiser.safetensors"
clothes_lord = clothes_1
clothes_name_list = ["高低领婚纱"]
old_list_clothes = [clothes_1]
list_clothes = [f"{i}. {clothes}--{name}" for i, (clothes, name) in enumerate(zip(old_list_clothes,clothes_name_list),start=1)]
clothes_lord_model_Strength = 0.85
clothes_lord_cilp_Strength = 1

"""色色"""
sex_1="Caught NTR-Sex-IL_NAI_PY.safetensors"
sex_lord = sex_1
sex_name_list = ["色色"]
old_list_sex = [sex_1]
list_sex = [f"{i}. {sex}--{name}" for i, (sex, name) in enumerate(zip(old_list_sex,sex_name_list),start=1)]
sex_lord_model_Strength = 0.6
sex_lord_cilp_Strength = 1

"""其他1"""
other_1 ="2725219?type=Model&format.safetensors"
other_2 ="2655999?type=Model&format.safetensors"
old_list_other= [other_1, other_2]
other_1_lord = other_1
other_name_list = ["眼睛修复", "手部修复"]

list_other_1 = [f"{i}. {other}--{name}" for i, (other, name) in enumerate(zip(old_list_other,other_name_list),start=1)]
other_1_lord_model_Strength = 0.4
other_1_lord_cilp_Strength = 1

"""其他2"""

other_2_lord = other_2
other_2_lord_model_Strength = 0.4
other_2_lord_cilp_Strength = 1

"""自定义工作流判断变量"""

custom_workflow_enabled = False # 这个变量用来判断是否启用自定义工作流，默认为False表示未启用。
custom_workflow_style_lord_enabled = False # 这个变量用来判断自定义工作流里风格lord的功能是否启用，默认为False表示未启用。
custom_workflow_character_lord_enabled = False # 这个变量用来判断自定义工作流里角色lord的功能是否启用，默认为False表示未启用。
custom_workflow_clothes_lord_enabled = False # 这个变量用来判断自定义工作流里衣服lord的功能是否启用，默认为False表示未启用。
custom_workflow_sex_lord_enabled = False # 这个变量用来判断自定义工作流里色色lord的功能是否启用，默认为False表示未启用。
custom_workflow_other_1_lord_enabled = False # 这个变量用来判断自定义工作流里其他1lord的功能是否启用，默认为False表示未启用。
custom_workflow_other_2_lord_enabled = False # 这个变量用来判断自定义工作流里其他2lord的功能是否启用，默认为False表示未启用。


"""图片路径"""
image_path = "data/plugin_data/astrbot_plugin_comfyui/images"
@register("ComfyUI_qqbot", "junxiang255", "一个简单的ComfyUIapi_sdxl插件", "1.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        
    @filter.command("查看系统信息")
    async def ComfyUI(self, event: AstrMessageEvent):
        client = ComfyUIClient("http://127.0.0.1:6006")
        ComfyUI_system = client.get_system_stats()
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 
        logger.info(message_chain)
        yield event.plain_result(f"系统是: {ComfyUI_system['system']['os']}")
        yield event.plain_result(f"显卡是: {ComfyUI_system['devices'][0]['name']}")
    @filter.command("查看模型强度")
    async def sdxl_loar(self, event: AstrMessageEvent):
        # builder = WorkflowBuilder()
        yield event.plain_result(f"正在加载SDXL LoRA模型...")
        yield event.plain_result(f"""当前lora模型:\n风格lord:{style_lord},模型力度:{style_lord_model_Strength},cilp力度:{style_lord_cilp_Strength}
                                 \n角色lord:{character_lord},模型力度:{character_lord_model_Strength},cilp力度:{character_lord_cilp_Strength}
                                 \n衣服lord:{clothes_lord},模型力度:{clothes_lord_model_Strength},cilp力度:{clothes_lord_cilp_Strength}
                                 \n色色lord:{sex_lord},模型力度:{sex_lord_model_Strength},cilp力度:{sex_lord_cilp_Strength}
                                 \n其他lord_1:{other_1_lord},模型力度:{other_1_lord_model_Strength},cilp力度:{other_1_lord_cilp_Strength}
                                 \n其他lord_2:{other_2_lord},模型力度:{other_2_lord_model_Strength},cilp力度:{other_2_lord_cilp_Strength}""")
    

    @filter.command_group("模型")
    def loar(self):
        pass
    @loar.group("calc")
    def calc(self):
        pass
    @loar.command("向导")
    async def help(self, event: AstrMessageEvent):
        
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 
        logger.info(message_chain)
        yield event.plain_result(f"这是LoRA模型的命令，您可以在这里实现浏览更换LoRA模型的功能。")
        yield event.plain_result(f"您想要浏览什么类型的LoRA模型？（风格、角色、衣服、色色、其他1、其他2）")
        yield event.plain_result(f"请回复对应的英文\nstyle---风格\ncharacter---角色\nclothes---衣服\nsex---色色\nother---其他")
        yield event.plain_result(f"例如，回复/loar_replace style 表示风格LoRA模型。\n{list_style}")
    @loar.command("风格")
    async def browse_style(self, event: AstrMessageEvent):
        
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 
        logger.info(message_chain)
        yield event.plain_result(f"正在获取风格LoRA模型文件列表")
        yield event.plain_result(f"\n".join(list_style))
        
    @loar.command("角色")
    async def browse_character(self, event: AstrMessageEvent):
        yield event.plain_result(f"正在获取角色LoRA模型文件列表")
        yield event.plain_result(f"当前数据库里有{len(list_character)}个角色LoRA模型")
        yield event.plain_result(f"\n".join(list_character))
        
        yield event.plain_result(f"请回复你想要使用哪个角色LoRA模型，例如回复/模型更换 角色 2 表示使用九条都这个角色LoRA模型")
    
    @loar.command("衣服")
    async def browse_clothes(self, event: AstrMessageEvent):
        yield event.plain_result(f"正在获取衣服LoRA模型文件列表")
        yield event.plain_result(f"\n".join(list_clothes))
    @loar.command("色色")
    async def browse_sex(self, event: AstrMessageEvent):
        yield event.plain_result(f"正在获取色色LoRA模型文件列表")
        yield event.plain_result(f"\n".join(list_sex))
    @loar.command("其他")
    async def browse_other(self, event: AstrMessageEvent):
        yield event.plain_result(f"正在获取其他1 LoRA模型文件列表")
        yield event.plain_result(f"\n".join(list_other_1))
    @filter.command("帮助")
    async def comfyui_help(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 
        yield event.plain_result("可用命令：/comfyui_system - 查看系统信息\n/sdxl [提示词] - 使用SDXL模型生成图片，提示词为用户输入的文本\n/sdxl_loar - 查看当前加载的SDXL LoRA模型及其参数\n/loar_replace - 浏览更换LoRA模型")
    @filter.command_group("模型更换")
    def loar_replace(self):
        pass
    @loar_replace.group("calc")
    def calc(self):
        pass
    @loar_replace.command("角色")
    async def replace_character1(self, event: AstrMessageEvent,Model_number: int):

        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 
        logger.info(message_chain) 
        if Model_number < 1 or Model_number > len(list_character):
            yield event.plain_result(f"无效的模型编号，请输入1到{len(list_character)}之间的数字")
        else:
            yield event.plain_result(f"正在更换角色LoRA模型")
            global character_lord
            character_lord = old_list_character[Model_number-1]
            yield event.plain_result(f"角色LoRA模型已更换为{list_character[Model_number-1]}")
            return
    @filter.command_group("自定义工作流")
    def custom_workflow(self):
        
        pass

    @custom_workflow.group("calc")
    def calc(self):
        pass
    @custom_workflow.command("启用")
    async def custom_workflow_enable(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链
        logger.info(message_chain)
        global custom_workflow_enabled
        custom_workflow_enabled = True
        yield event.plain_result(f"已启用自定义工作流，您可以通过/自定义工作流 帮助 来查看如何启用或禁用自定义工作流里各个lord的功能")
    @custom_workflow.command("禁用")
    async def custom_workflow_disable(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链
        logger.info(message_chain)
        global custom_workflow_enabled
        custom_workflow_enabled = False
        yield event.plain_result(f"已禁用自定义工作流，生成图片时将不使用您自定义的工作流")

    @custom_workflow.command("帮助")
    async def custom_workflow_help(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链
        logger.info(message_chain)
        yield event.plain_result(f"这是自定义工作流的命令，您可以在这里启用或禁用自定义工作流里各个lord的功能，这些lord的功能是基于SDXL LoRA模型的，启用后会在生成图片时将对应的LoRA模型加入到工作流里，增强图片的对应方面的表现。")
        yield event.plain_result(f"您想要启用或禁用哪个lord的功能？")
        yield event.plain_result(f"一共有6个lord模型，分别是风格、角色、衣服、色色、其他1、其他2")
        yield event.plain_result(f"例如，回复/自定义工作流 角色模型 启用 表示启用角色lord的功能。")
        yield event.plain_result(f"例如，回复/自定义工作流 角色模型 禁用 表示禁用角色lord的功能。")
    @custom_workflow.command("角色模型")
    async def custom_workflow_character(self, event: AstrMessageEvent,whether:str):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 
        logger.info(message_chain) 
        global custom_workflow_character_lord_enabled
        if whether=="启用":
            custom_workflow_character_lord_enabled = True
            yield event.plain_result(f"已启用自定义工作流里的角色lord功能")
        elif whether=="禁用":
            custom_workflow_character_lord_enabled = False
            yield event.plain_result(f"已禁用自定义工作流里的角色lord功能")
        else:
            yield event.plain_result(f"无效的输入，请输入启用/禁用")
       
    @custom_workflow.command("风格模型")
    async def custom_workflow_style(self, event: AstrMessageEvent,whether:str):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 
        logger.info(message_chain) 
        global custom_workflow_style_lord_enabled
        if whether=="启用":
            custom_workflow_style_lord_enabled = True
            yield event.plain_result(f"已启用自定义工作流里的风格lord功能")
        elif whether=="禁用":
            custom_workflow_style_lord_enabled = False
            yield event.plain_result(f"已禁用自定义工作流里的风格lord功能")
        else:
            yield event.plain_result(f"无效的输入，请输入启用/禁用")
    @custom_workflow.command("衣服模型")
    async def custom_workflow_clothes(self, event: AstrMessageEvent,whether:str):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链
        logger.info(message_chain)
        global custom_workflow_clothes_lord_enabled
        if whether=="启用":
            custom_workflow_clothes_lord_enabled = True
            yield event.plain_result(f"已启用自定义工作流里的衣服lord功能")
        elif whether=="禁用":
            custom_workflow_clothes_lord_enabled = False
            yield event.plain_result(f"已禁用自定义工作流里的衣服lord功能")
        else:
            yield event.plain_result(f"无效的输入，请输入启用/禁用")
    @custom_workflow.command("色色模型")
    async def custom_workflow_sex(self, event: AstrMessageEvent,whether:str):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链
        logger.info(message_chain)
        global custom_workflow_sex_lord_enabled
        if whether=="启用":
            custom_workflow_sex_lord_enabled = True
            yield event.plain_result(f"已启用自定义工作流里的色色lord功能")
        elif whether=="禁用":
            custom_workflow_sex_lord_enabled = False
            yield event.plain_result(f"已禁用自定义工作流里的色色lord功能")
        else:
            yield event.plain_result(f"无效的输入，请输入启用/禁用")
    @custom_workflow.command("其他1模型")
    async def custom_workflow_other_1(self, event: AstrMessageEvent,whether:str):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链
        logger.info(message_chain)
        global custom_workflow_other_1_lord_enabled
        if whether=="启用":
            custom_workflow_other_1_lord_enabled = True
            yield event.plain_result(f"已启用自定义工作流里的其他1lord功能")
        elif whether=="禁用":
            custom_workflow_other_1_lord_enabled = False
            yield event.plain_result(f"已禁用自定义工作流里的其他1lord功能")
        else:
            yield event.plain_result(f"无效的输入，请输入启用/禁用")
    @custom_workflow.command("其他2模型")
    async def custom_workflow_other_2(self, event: AstrMessageEvent,whether:str):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链
        logger.info(message_chain)
        global custom_workflow_other_2_lord_enabled
        if whether=="启用":
            custom_workflow_other_2_lord_enabled = True
            yield event.plain_result(f"已启用自定义工作流里的其他2lord功能")
        elif whether=="禁用":
            custom_workflow_other_2_lord_enabled = False
            yield event.plain_result(f"已禁用自定义工作流里的其他2lord功能")
        else:
            yield event.plain_result(f"无效的输入，请输入启用/禁用")

    @filter.command("生成图片")
    async def qqbot_ComfyUI(self, event: AstrMessageEvent,):
        
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        """正向表达式去除命令部分，得到纯提示词"""
        clean_prompt = re.sub(r'^生成图片\s*', '',message_str )
        
        client = ComfyUIClient("http://127.0.0.1:6006")
        """非自定义工作流"""
        builder = WorkflowBuilder()
        """自定义工作流"""
        custom_builder = custom_WorkflowBuilder()
        """向用户展示纯提示词"""
        yield event.plain_result(clean_prompt)
        """判断是否启用自定义工作流并构建"""
        if custom_workflow_enabled==False:
            builder.add_checkpoint_loader(checkpoint_loader)
            builder.add_lord_style(style_lord, style_lord_model_Strength, style_lord_cilp_Strength)
            """风格"""
            builder.add_load_character(character_lord, character_lord_model_Strength, character_lord_cilp_Strength)
            """人物"""
            builder.add_load_clothes(clothes_lord, clothes_lord_model_Strength, clothes_lord_cilp_Strength)
            """衣服"""
            builder.add_load_sex(sex_lord, sex_lord_model_Strength, sex_lord_cilp_Strength)
            """色色lord"""
            builder.add_load_Other_1(other_1_lord, other_1_lord_model_Strength, other_1_lord_cilp_Strength)
            """其他lord_1"""
            builder.add_load_Other_2(other_2_lord, other_2_lord_model_Strength, other_2_lord_cilp_Strength)
            """其他lord_2"""
            builder.add_ksampler()
            builder.add_text_encoder(clean_prompt)
            builder.add_Negative_text_encoder(
                "censored,mosaic censoring,bar censor,signature,username,logo,bad hands,mutated hands,watermark,missing limb,missing finger,")
            builder.add_Latent(1024, 1600, 1)
            builder.add_vae_decode()
            builder.add_save_image()
            builder.build()
            workflow = builder.build()
        elif custom_workflow_enabled==True:
            """底模不可去除"""
            custom_builder.add_checkpoint_loader(checkpoint_loader)

            """判断自定义工作流里各个lord的功能是否启用并添加对应的节点"""
            if custom_workflow_style_lord_enabled==True:
                custom_builder.add_lord_style(style_lord, style_lord_model_Strength, style_lord_cilp_Strength)
                """风格lord"""
            if custom_workflow_character_lord_enabled==True:
                custom_builder.add_load_character(character_lord, character_lord_model_Strength, character_lord_cilp_Strength)
                """角色lord"""
            if custom_workflow_clothes_lord_enabled==True:
                custom_builder.add_load_clothes(clothes_lord, clothes_lord_model_Strength, clothes_lord_cilp_Strength)
                """衣服lord"""
            if custom_workflow_sex_lord_enabled==True:
                custom_builder.add_load_sex(sex_lord, sex_lord_model_Strength, sex_lord_cilp_Strength)
                """色色lord"""
            if custom_workflow_other_1_lord_enabled==True:
                custom_builder.add_load_Other_1(other_1_lord, other_1_lord_model_Strength, other_1_lord_cilp_Strength)
                """其他lord_1"""
            if custom_workflow_other_2_lord_enabled==True:
                custom_builder.add_load_Other_2(other_2_lord, other_2_lord_model_Strength, other_2_lord_cilp_Strength)
                """其他lord_2"""
            """-------分隔线-------"""
            """采样器不可去除"""
            custom_builder.add_ksampler()
            """提示词和反向提示词不可去除"""
            custom_builder.add_text_encoder(clean_prompt)# 将用户输入的提示词添加到工作流里
            custom_builder.add_Negative_text_encoder(
                "censored,mosaic censoring,bar censor,signature,username,logo,bad hands,mutated hands,watermark,missing limb,missing finger,")# 将反向提示词添加到工作流里
            custom_builder.add_Latent(1024, 1600, 1)# 添加latent节点,参数分别是宽、高、生成图片的数量
            custom_builder.add_vae_decode()# 添加vae解码节点
            custom_builder.add_save_image()# 添加保存图片节点
            custom_builder.build()# 构建工作流
            workflow = custom_builder.build() # 获取构建好的工作流
        print(workflow)# 打印工作流信息到控制台，方便调试
        prompt_id = client.submit_workflow(workflow)# 将工作流提交到ComfyUI服务器，并获取返回的prompt_id，这个ID可以用来查询生成结果
        yield event.plain_result(f"任务已提交，ID: {prompt_id}")# 向用户展示任务提交成功的消息，并显示prompt_id
        result = client.wait_for_completion(prompt_id)# 等待工作流执行完成，并获取结果，result是一个包含生成状态和输出的字典
        print(result["status"])# 打印生成状态到控制台，方便调试
        if custom_workflow_enabled==True:# 根据是否启用自定义工作流来确定保存图片节点的ID，因为如果启用了自定义工作流，保存图片节点的位置可能会发生变化
            node_id = custom_builder.add_save_image() - 1 # 不-1这个会返回空节点
        elif custom_workflow_enabled==False:
            node_id =builder.add_save_image() - 1
        print(node_id)# 打印保存图片节点的ID到控制台，方便调试
        
        if result["status"]["status_str"] == "success":# 判断生成是否成功
            outputs = result["outputs"]


            output = outputs[f"{node_id}"]["images"]# 从结果里获取保存图片节点的输出，输出里包含了生成的图片信息，这里的key是保存图片节点的ID加上字符串"images"
            for image_info in output:# 遍历输出里的图片信息，理论上应该只有一张图，因为我们在添加latent节点时设置了生成图片的数量为1
                print(output)
                filename = image_info["filename"]
                image_data = client.download_image(filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_data)
                    yield event.plain_result(f"图片已生成并保存为 generated_{filename}")
                    yield event.image_result(f"{image_path}/generated_{filename}")
                
        
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
