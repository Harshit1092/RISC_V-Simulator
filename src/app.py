from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    content = file.read().decode('utf-8')
    
    prog_mc_file = request.form.get('prog_mc_file') == 'true'
    pipelining_enabled = request.form.get('pipelining_enabled') == 'true'
    forwarding_enabled = request.form.get('forwarding_enabled') == 'true'
    print_registers_each_cycle = request.form.get('print_registers_each_cycle') == 'true'
    print_pipeline_registers = request.form.get('print_pipeline_registers') == 'true'
    print_specific_pipeline_registers = request.form.get('print_specific_pipeline_registers') == 'true'
    number = request.form.get('number')
    data_cache = request.form.get('data_cache')
    data_cache_block = request.form.get('data_cache_block')
    data_associativity = request.form.get('data_associativity')
    data_ways = request.form.get('data_ways')
    inst_cache = request.form.get('inst_cache')
    inst_cache_block = request.form.get('inst_cache_block')
    inst_associativity = request.form.get('inst_associativity')
    inst_ways = request.form.get('inst_ways')
    policy = request.form.get('policy')
    
    # Do something with the file and the boolean values
    demo = open('demofile.txt','w')
    demo.write(content)
    demo.close()
    f  = open("input.txt",'w')
    f.close()
    f = open('input.txt','a')
    f.write(str(pipelining_enabled)+'\n')
    f.write(str(forwarding_enabled)+'\n')
    f.write(str(print_registers_each_cycle)+'\n')
    f.write(str(print_pipeline_registers)+'\n')
    # f.write(str(print_specific_pipeline_registers[0]) + ' ' + str(print_specific_pipeline_registers[1]) + '\n')
    f.write(str(print_specific_pipeline_registers) + ' ' + str(number) + '\n')

    f.close()
    
    f = open('cacheInput.txt','w')
    f.close()
    f = open('cacheInput.txt','a')
    f.write(str(data_cache)+' ')
    f.write(str(data_cache_block)+' ')
    f.write(str(data_associativity)+' ')
    f.write(str(data_ways)+'\n')
    f.write(str(inst_cache)+' ')
    f.write(str(inst_cache_block)+' ')
    f.write(str(inst_associativity)+' ')
    f.write(str(inst_ways)+'\n')
    f.write(str(policy) + '\n')
    f.close()
    return jsonify({'message': 'File uploaded successfully'})


@app.route('/runScripts', methods=['POST'])
def run_Scripts():
    # print("HELLO0")
    # data = request.get_json()
    # arg = data.get('arg')
    # print(arg)
    # print("HELLO1")
    first = subprocess.run(['python','./main.py'])
    if first.returncode != 0:
        return jsonify({'error': 'Failed to execute first script'})
    
    # print("HELLO2")
    second = subprocess.run(['python','./jsonify.py'])
    if second.returncode != 0:
        return jsonify({'error' : 'Failed to execute second script'})
    # print("HELLO3")
    return jsonify({'request' : 'Both scripts executed successfully'})

if __name__=='__main__':
   app.run()