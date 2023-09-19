"""
Response time - dual-threaded
"""

from machine import Pin
import time
import random
import os
import json
import _thread


def get_params(param_file: str) -> dict:
    """Reads parameters from a JSON file."""

    if not is_regular_file(param_file):
        raise OSError(f"File {param_file} not found")

    with open(param_file) as f:
        params = json.load(f)

    return params

def is_regular_file(path: str) -> bool:
    """Checks if a regular file exists."""

    S_IFREG = 0x8000

    try:
        return os.stat(path)[0] & S_IFREG != 0
    except OSError:
        return False

def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)

def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)

def blinker(N: int) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)
        
led = Pin("LED", Pin.OUT)
def core0_thread():
    
    button01 = Pin(16, Pin.IN, Pin.PULL_UP)
    button02 = Pin(26, Pin.IN, Pin.PULL_UP)

    params = get_params("project02_flash.json")
    N: int = params["num_flash"]
    sample_ms = params["sample_ms"]
    on_ms = params["on_ms"]

    t1: list[float | None] = []
    t2: list[float | None] = []
    blinker(3)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t01 = None
        t02 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button01.value() == 0 and button02.value() == 0:
                t01 = time.ticks_diff(time.ticks_ms(), tic)
                t02 = t01
                led.low()
                break
            elif button01.value() == 0:
                t01 = time.ticks_diff(time.ticks_ms(), tic)
                if button02.value() == 0:
                    t02 = time.ticks_diff(time.ticks_ms(), tic)
                    led.low()
                    break
                
            elif button02.value() == 0:
                t02 = time.ticks_diff(time.ticks_ms(), tic)
                if button01.value() == 0:
                    t01 = time.ticks_diff(time.ticks_ms(), tic)
                    led.low()
                    break
            
            
        t1.append(t01)
        t2.append(t02)

        led.low()

    blinker(5)

    # %% collate results
    misses1 = t1.count(None)
    print(f"Player 1 missed the light {misses1} / {N} times")
    misses2 = t2.count(None)
    print(f"Player 2 missed the light {misses2} / {N} times")
    score_1 = N - misses1
    score_2 = N - misses2

    t1_good = [x for x in t1 if x is not None]
    t2_good = [x for x in t2 if x is not None]

    print(t1_good)
    print(t2_good)

    # calculate the average, min, max response time
    if bool(t1_good)==0:
        max_time1 = None
        min_time1 = None
        avg_time1 = None
    else:
        max_time1 = max(t1_good)
        min_time1 = min(t1_good)
        avg_time1 = sum(t1_good)/len(t1_good)
    if bool(t2_good)==0:
        max_time2 = None
        min_time2 = None
        avg_time2 = None
    else:
        max_time2 = max(t2_good)
        min_time2 = min(t2_good)
        avg_time2 = sum(t2_good)/len(t2_good)

    # change the params
    params["min_response_time_1"] = min_time1
    params["max_response_time_1"] = max_time1
    params["avg_response_time_1"] = avg_time1
    params["score_1"] = f" {score_1} / {N}"

    params["min_response_time_2"] = min_time2
    params["max_response_time_2"] = max_time2
    params["avg_response_time_2"] = avg_time2
    params["score_2"] = f" {score_2} / {N}"

    # write into the json file
    try:
        with open("project02_flash.json", "w") as json_file:
            json.dump(params, json_file)
        print("Parameter value updated successfully.")
    except OSError as e:
        print("Error writing to JSON file:", e)
        
def photocell_logger(N: int, sample_interval_s: float) -> None:
    """
    get raw uint16 values from photocell N times and save to JSON file

    Parameters
    ----------

    N: int
        number of samples to take
    """

    print("start light measurement thread")

    adc = machine.ADC(28)

    values: list[int] = []

    start_time: tuple[int] = time.localtime()

    for _ in range(N):
        values.append(adc.read_u16())
        time.sleep(sample_interval_s)

    end_time: tuple[int] = time.localtime()
    # please also log the end_time and sample interval in the JSON file
    #  i.e. two additional key, value in the dict

    data = {
        "light_uint16": values,
        "start_time": start_time,
    }

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"project02_intensity.json"

    print("light measurement done: write", filename)

    project01.write_json(filename, data)
    
# dual thread
second_thread = _thread.start_new_thread(photocell_logger, ())
 
core0_thread()
