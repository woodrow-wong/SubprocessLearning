import subprocess
import logging

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

    # 实时读取并记录输出
    while True:
        # 从标准输出读取一行
        output = process.stdout.readline()
        if output:
            output = output.strip()
            logger.info(output)

        # 检查进程是否结束
        return_code = process.poll()
        if return_code is not None:
            # 读取剩余输出
            for output in process.stdout.readlines():
                output = output.strip()
                logger.info(output)

            # 读取错误输出
            for error in process.stderr.readlines():
                error = error.strip()
                logger.error(error)

            # 记录完成信息并返回
            logger.info(f"命令执行完成，返回代码: {return_code}")
            return return_code

def main():
    print("Hello from subprocess-learning!")
    # 修改为使用shell模式执行echo命令
    execute_command("echo 这是一个测试命令", shell=True)
    
    # 或者使用内置的print函数来演示
    print("\n另一种方式测试输出:")
    import platform
    if platform.system() == "Windows":
        # Windows系统使用cmd命令
        execute_command(["cmd", "/c", "dir"], shell=True)
    else:
        # Linux/Mac系统使用ls命令
        execute_command(["ls", "-la"])


if __name__ == "__main__":
    main()
