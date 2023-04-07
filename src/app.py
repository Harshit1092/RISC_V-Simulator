from flask import Flask, request, jsonify
from flask_cors import CORS

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
    f.write(str(print_specific_pipeline_registers)+'\n')
    f.close()
    return jsonify({'message': 'File uploaded successfully'})


if __name__=='__main__':
   app.run()