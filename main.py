import subprocess
import logging
import platform

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def execute_command(cmd, working_dir=None, shell=False):
    """
    执行命令并实时获取输出
    
    参数:
    cmd: list 或 str - 要执行的命令
    working_dir: str - 工作目录，默认为None
    shell: bool - 是否通过shell执行命令，Windows环境下执行内置命令需设为True
    
    返回:
    int - 命令的返回码
    """
    # 执行命令并等待完成
    process = subprocess.Popen(
        cmd,
        cwd=working_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=shell  # 添加shell参数
    )

    # # 实时读取并记录输出
    # while True:  # 循环确保读取所有输出
        # 从标准输出读取一行
    capture = process.stdout.readlines()
    
    # # 检查是否有输出内容
    # if output:  # 恢复条件检查，防止空行导致无限循环
    for line in capture:
        output = line.strip()
        logger.info(output)
        
        # # 检查进程是否结束
        # return_code = process.poll()
        # if return_code is not None:
        #     # 如果没有更多输出且进程已结束，跳出循环
        #     if not output:  # 当readline()返回空且进程已结束时，退出循环
        #         break
                
        #     # 读取剩余输出
        #     for output in process.stdout.readlines():
        #         output = output.strip()
        #         logger.info(output)

        #     # 读取错误输出
        #     for error in process.stderr.readlines():
        #         error = error.strip()
        #         logger.error(error)

        #     # 记录完成信息并返回
        #     logger.info(f"命令执行完成，返回代码: {return_code}")
        #     return return_code

def main():
    print("Hello from subprocess-learning!")
    print("=" * 50)
    
    # print("\n示例1: 基本命令执行")
    # print("-" * 30)
    # # 基本的echo命令
    # execute_command("echo 这是一个基本的测试命令", shell=True)
    
    # print("\n示例2: 运行系统命令查看信息")
    # print("-" * 30)
    # # 查看系统信息
    # execute_command("systeminfo | findstr /B /C:\"OS 名称\" /C:\"OS 版本\"", shell=True)
    
    print("\n示例4: 持续输出命令")
    print("-" * 30)
    # ping命令会产生持续的输出，非常适合观察readline()的效果
    # 这里只ping 3次，以免等待时间过长
    if platform.system() == "Windows":
        execute_command("ping -n 3 127.0.0.1", shell=True)
    else:
        execute_command("ping -c 3 127.0.0.1", shell=True)
    
    # print("\n示例5: 执行目录列表命令")
    # print("-" * 30)
    # # 列出当前目录文件
    # if platform.system() == "Windows":
    #     execute_command("dir", shell=True)
    # else:
    #     execute_command("ls -la", shell=True)
    
    # print("\n示例6: 使用错误的命令")
    # print("-" * 30)
    # # 执行一个不存在的命令，观察错误处理
    # execute_command("non_existent_command", shell=True)
    
    # print("\n示例7: 多行输出命令")
    # print("-" * 30)
    # # 执行产生多行输出的命令
    # if platform.system() == "Windows":
    #     execute_command("ipconfig /all", shell=True)
    # else:
    #     execute_command("ifconfig", shell=True)
    
    # print("\n示例8: 执行Python代码")
    # print("-" * 30)
    # # 使用Python执行一个简单的脚本
    # python_cmd = 'python -c "import time; print(\'开始执行\'); time.sleep(1); print(\'执行中...\'); time.sleep(1); print(\'执行结束\')"'
    # execute_command(python_cmd, shell=True)

    # print("\n所有示例执行完毕!")


if __name__ == "__main__":
    main()
