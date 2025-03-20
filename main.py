import subprocess
import logging
import platform
import selectors  # 在Unix系统上使用
import threading  # 添加线程支持
import sys        # 用于检测操作系统

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def execute_command(cmd, working_dir=None, shell=False):
    """
    执行命令并实时获取标准输出和错误输出
    
    参数:
    cmd: list 或 str - 要执行的命令
    working_dir: str - 工作目录，默认为None
    shell: bool - 是否通过shell执行命令，Windows环境下执行内置命令需设为True
    
    返回:
    int - 命令的返回码
    """
    print(f"准备执行命令: {cmd}")
    print("创建子进程并设置管道...")
    
    # 执行命令并建立管道
    process = subprocess.Popen(
        cmd,
        cwd=working_dir,
        stdout=subprocess.PIPE,  # 创建标准输出管道
        stderr=subprocess.PIPE,  # 创建标准错误管道
        text=True,               # 将字节流自动解码为文本
        shell=shell
    )
    
    print(f"子进程已启动，PID: {process.pid}")
    print("开始从管道读取输出...")
    
    # 判断操作系统
    is_windows = sys.platform.startswith('win')
    
    if is_windows:
        # Windows方案：使用线程分别读取stdout和stderr
        print("\n=== 使用线程分别读取stdout和stderr（Windows平台）===")
        
        # 定义线程函数：读取流并按行处理
        def read_stream(stream, stream_name, logger_func):
            print(f"开始读取{stream_name}...")
            for line in stream:
                line = line.strip()
                print(f"收到{stream_name} ({len(line)} 字节): {line}")
                logger_func(line)
            print(f"{stream_name}读取完毕")
        
        # 创建并启动两个线程
        stdout_thread = threading.Thread(
            target=read_stream, 
            args=(process.stdout, "标准输出", logger.info)
        )
        stderr_thread = threading.Thread(
            target=read_stream, 
            args=(process.stderr, "错误输出", logger.error)
        )
        
        stdout_thread.start()
        stderr_thread.start()
        
        # 等待子进程结束
        return_code = process.wait()
        print(f"子进程已结束，返回码: {return_code}")
        
        # 等待读取线程结束
        stdout_thread.join()
        stderr_thread.join()
        
        print(f"命令执行完成，退出码: {return_code}")
        return return_code
    else:
        # Unix方案：使用selectors同时监控stdout和stderr
        print("\n=== 使用selectors同时监控stdout和stderr (Unix平台) ===")

        # 创建selector对象
        sel = selectors.DefaultSelector()

        # 注册stdout和stderr到selector
        sel.register(process.stdout, selectors.EVENT_READ, 'stdout')
        sel.register(process.stderr, selectors.EVENT_READ, 'stderr')

        # 循环读取输出
        while True:
            events = sel.select(timeout=0.1)
            
            for key, _ in events:
                stream = key.fileobj
                name = key.data
            
                line = stream.readline()
                if line:
                    line = line.strip()
                    if name == 'stdout':
                        print(f"收到标准输出 ({len(line)} 字节): {line}")
                        logger.info(line)
                    else:
                        print(f"收到错误输出 ({len(line)} 字节): {line}")
                        logger.error(line)
            
            # 检查进程是否结束
            return_code = process.poll()
            if return_code is not None:
                print(f"检测到子进程已结束，返回码: {return_code}")         
                if events:
                    continue          
                # 检查是否还有剩余输出
                remaining_output = process.stdout.read()
                if remaining_output:
                    print(f"读取剩余标准输出 ({len(remaining_output)} 字节)")
                    for line in remaining_output.splitlines():
                        logger.info(line)
                
                remaining_error = process.stderr.read()
                if remaining_error:
                    print(f"读取剩余错误输出 ({len(remaining_error)} 字节)")
                    for line in remaining_error.splitlines():
                        logger.error(line)
                
            if not events and not remaining_output and not remaining_error:
                print("没有更多输出，退出读取循环")
                break

        # 关闭selector
        sel.close()
    
    print(f"命令执行完成，退出码: {return_code}")
    return return_code

    # 方法2: 将错误输出重定向到标准输出 (更简单但区分不了stdout和stderr)
    # process = subprocess.Popen(
    #     cmd,
    #     cwd=working_dir,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.STDOUT,  # 将stderr重定向到stdout
    #     text=True,
    #     shell=shell
    # )
    # 
    # for line in process.stdout:
    #     logger.info(line.strip())
    # 
    # return process.wait()

def main():
    print("Hello from subprocess-learning!")
    print("=" * 50)
    
    # print("\n示例1: 基本命令执行")
    # print("-" * 30)
    # # 基本的echo命令
    # exe# 方法2: 将错误输出重定向到标准输出 (更简单但区分不了stdout和stderr)
    # process = subprocess.Popen(
    #     cmd,
    #     cwd=working_dir,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.STDOUT,  # 将stderr重定向到stdout
    #     text=True,
    #     shell=shell
    # )
    # 
    # for line in process.stdout:
    #     logger.info(line.strip())
    # 
    # return process.wait()

execute_command("echo 这是一个基本的测试命令", shell=True)
    
    # print("\n示例2: 运行系统命令查看信息")
    # print("-" * 30)


    # # exe# 方法2: 将错误输出重定向到标准输出 (更简单但区分不了stdout和stderr)
    # process = subprocess.Popen(
    #     cmd,
    #     cwd=working_dir,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.STDOUT,  # 将stderr重定向到stdout
    #     text=True,
    #     shell=shell
    # )
    # 
    # for line in process.stdout:
    #     logger.info(line.strip())
    # 
    # return process.wait()

    
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
