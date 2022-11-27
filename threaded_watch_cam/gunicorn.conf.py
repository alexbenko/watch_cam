from dotenv import load_dotenv
import os
import multiprocessing
load_dotenv()
host = os.getenv('HOST', '0.0.0.0')
port = os.getenv('PORT', 5000)

bind = f'{host}:{port}'
timeout = 120
#TODO: Read gunicorn docs and figure out if this is necessary
#num_of_cores = multiprocessing.cpu_count()
#num_of_workers = os.getenv('GUNICORN_WORKERS', ( num_of_cores * 2) + 1)

#worker_class = 'gevent' #server uses 3-4 threads
#preload_app = os.getenv('PRE_LOAD', 'True').lower() in ('true', '1', 't')

#PER GUNICORN DOCS, number of workers should be: (2 x $num_cores) + 1
#workers = num_of_workers
#PER DOCS: Threads should be: 2-4 x $(NUM_CORES)
#threads = num_of_cores * 2