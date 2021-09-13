import argparse
import time
import requests

url = 'http://0.0.0.0:8080/variable'

def test_update(args):
    ret = __get_all_workers(args.num_workers, url, {'var': args.key})
    __print_responses(ret)
    
    if args.key == 'sighup_data':
        time.sleep(5)
    else:
        data = {}
        data[args.key] = args.value
        requests.put(url, json=data)

    ret = __get_all_workers(args.num_workers, url, {'var': args.key})
    __print_responses(ret)

def __get_all_workers(num_workers, url, params, body=None):
    print('Getting data from workers...')
    responses = {}
    if body:
        print('put') 
    else:
        while len(responses) < num_workers:
            ret = requests.get(url, params=params)
            res = ret.text.split('|')
            worker_pid = res[0].strip()
            worker_value = res[1].strip()
            if worker_pid not in responses:
                responses[worker_pid] = worker_value 
        return responses

def __print_responses(responses):
    for k, v in responses.items():
        print(f'[Worker {k}] {v}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()    
    parser.add_argument('--key', type=str, required=True)
    parser.add_argument('--value', type=str, required=True)
    parser.add_argument('--num-workers', type=int, default=5)
    args = parser.parse_args()
    test_update(args)
