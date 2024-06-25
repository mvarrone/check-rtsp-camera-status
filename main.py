import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import subprocess
import sys
from typing import List, Dict, Tuple, Union


def check_camera(
    camera_config: Dict[str, Union[str, int]]
) -> Tuple[bool, float, str, Union[str, int, None], str, str]:
    protocol = camera_config.get("protocol")
    username = camera_config.get("username")
    password = camera_config.get("password")
    domain = camera_config.get("domain")
    port = camera_config.get("port")
    path = camera_config.get("path")
    camera_number = camera_config.get("camera_number")

    url = f"{protocol}://{username}:{password}@{domain}:{port}{path}{camera_number}"
    start_time = time.time()
    is_up = False

    try:
        # Use ffmpeg to try to access the camera stream and capture detailed errors
        command = [
            "ffmpeg",
            "-rtsp_transport",
            "tcp",
            "-i",
            url,
            "-vframes",
            "1",
            "-f",
            "null",
            "-",
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stderr_output = result.stderr.decode()

        if result.returncode == 0:
            is_up = True
            error_msg = ""
            error_code = 0
        else:
            if "401 Unauthorized" in stderr_output:
                error_msg = "401 Unauthorized"
                error_code = 401
            elif "404 Not Found" in stderr_output:
                error_msg = "404 Not Found"
                error_code = 404
            else:
                error_msg = f"Other error: {stderr_output}"
                error_code = -1

        exec_time = time.time() - start_time
        return is_up, exec_time, domain, camera_number, url, error_msg, error_code

    except Exception as e:
        error_msg = str(e)
        exec_time = time.time() - start_time
        return is_up, exec_time, domain, camera_number, url, error_msg, error_code


def print_stats(
    total_cameras, cameras_up, cameras_down, total_response_time, status_up, status_down
) -> None:
    print(f"Total of cameras checked: {total_cameras}")
    print(f"Cameras up: {cameras_up}")
    print(f"Cameras down: {cameras_down}")

    if total_cameras > 0:
        percentage_cameras_up = (cameras_up / total_cameras) * 100
        percentage_cameras_down = (cameras_down / total_cameras) * 100
        print(f"Percentage of cameras up: {percentage_cameras_up:.2f} %")
        print(f"Percentage of cameras down: {percentage_cameras_down:.2f} %")

    if cameras_up > 0:
        avg_response_time = total_response_time / cameras_up
        print(f"Average response time for cameras up: {avg_response_time:.2f} s")

    print("\nStatus up")
    for item in status_up:
        print(item)

    print("\nStatus down")
    for item in status_down:
        print(item)


def load_credentials(filename: str) -> Tuple[List[Dict], Dict[str, str]]:
    error = {}
    try:
        # Load parameters from JSON file
        with open(filename, "r") as file:
            camera_configs: list = json.load(file)
    except Exception as e:
        camera_configs = []
        error = {"error_msg": str(e)}
        return camera_configs, error
    return camera_configs, error


def main() -> None:
    # 1. Load credentials
    filename = "./credentials.json"
    camera_configs, error = load_credentials(filename)
    if error:
        print(error.get("error_msg"))
        sys.exit(1)

    # 2. Commence checking the cameras' status
    # 2a. Setting some variables for later stats
    total_cameras = len(camera_configs)
    cameras_up = 0
    cameras_checked = 0
    total_response_time = 0
    status_up = []
    status_down = []

    # 2b. Implementing parallel execution for all cameras
    with ProcessPoolExecutor() as executor:
        # Submit URL checks as concurrent tasks
        future_to_config = {
            executor.submit(check_camera, config): config for config in camera_configs
        }
        for future in as_completed(future_to_config):
            cameras_checked += 1
            config = future_to_config[future]
            try:
                is_up, exec_time, domain, camera_number, url, error_msg, error_code = (
                    future.result()
                )
                if is_up:
                    cameras_up += 1
                    total_response_time += exec_time
                    status_up.append(
                        {"domain": domain, "url": url, "camera": camera_number}
                    )
                else:
                    status_down.append(
                        {
                            "domain": domain,
                            "url": url,
                            "camera": camera_number,
                            "error_msg": error_msg,
                            "error_code": error_code,
                        }
                    )
            except Exception as exc:
                print(f"Error occurred while checking {config}: {exc}")

    # 3. Print stats
    cameras_down = total_cameras - cameras_up
    print_stats(
        total_cameras,
        cameras_up,
        cameras_down,
        total_response_time,
        status_up,
        status_down,
    )


if __name__ == "__main__":
    start_total = time.time()
    main()
    end_total = time.time() - start_total
    print(f"\nTotal script execution time: {end_total:.2f} s")
