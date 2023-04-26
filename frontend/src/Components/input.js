import React, {useState} from "react";

function Input() {
    const options = {
        0:"Fully Associative", 1:"Direct Mapped", 2:"Set Associative"
    }
    const options1 = {
        0:"LRU", 1:"FIFO", 2:"Random", 3:"LFU", 4:"LIFO"
    }
    const [pipeliningEnabled, setPipeliningEnabled] = useState(false);
    const [forwardingEnabled, setForwardingEnabled] = useState(false);
    const [printRegistersEachCycle, setPrintRegistersEachCycle] = useState(false);
    const [printPipelineRegisters, setPrintPipelineRegisters] = useState(false);
    const [printSpecificPipelineRegisters, setPrintSpecificPipelineRegisters] = useState(false);
    const [instructionNumber, setInstructionNumber] = useState(-1);
    const [selectedFile, setSelectedFile] = useState(null);
    const [dataCache, setDataCache] = useState(32);
    const [dataCacheBlock, setDataCacheBlock] = useState(4);
    const [associativityData, setassociativityData] = useState(2);
    const [waysData, setWaysData] = useState(2);
    const [instCache, setInstCache] = useState(32);
    const [instCacheBlock, setInstCacheBlock] = useState(4);
    const [associativityInst, setassociativityInst] = useState(2);
    const [waysInst, setWaysInst] = useState(2);
    const [policy, setPolicy] = useState(0);
    
        function handleFileInput(e) {
          setSelectedFile(e.target.files[0]);
        };

    const handlePipeliningEnabled = () => {
        setPipeliningEnabled(!pipeliningEnabled);
    };

    const handleForwardingEnabled = () => {
        setForwardingEnabled(!forwardingEnabled);
    };

    const handlePrintRegistersEachCycle = () => {
        setPrintRegistersEachCycle(!printRegistersEachCycle);
    };

    const handlePrintPipelineRegisters = () => {
        setPrintPipelineRegisters(!printPipelineRegisters);
    };

    const handlePrintSpecificPipelineRegisters = () => {
        setPrintSpecificPipelineRegisters(!printSpecificPipelineRegisters);
    };

    const handleInstructionNumber = (event) => {
        setInstructionNumber(event.target.value);
    };
    const handleDataCache = (e) => {
        setDataCache(e.target.value);
    }
    const handleDataCacheBlock = (e) => {
        setDataCacheBlock(e.target.value);
    }
    const handleassociativityData = (e) => {
        setassociativityData(e.target.value);
    };
    const handleWaysData = (e) => {
        setWaysData(e.target.value);
    }
    const handleDataCache1 = (e) => {
        setInstCache(e.target.value);
    }
    const handleDataCacheBlock1 = (e) => {
        setInstCacheBlock(e.target.value);
    }
    const handleassociativityData1 = (e) => {
        setassociativityInst(e.target.value);
    };
    const handleWaysData1 = (e) => {
        setWaysInst(e.target.value);
    }
    const handlePolicy = (e) => {
        setPolicy(e.target.value);
    }

    const handleSubmit = () => {
        if (!selectedFile) {
            alert("Please select a file.");
            return;
        }
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('pipelining_enabled', pipeliningEnabled);
        formData.append('forwarding_enabled', forwardingEnabled);
        formData.append('print_registers_each_cycle', printRegistersEachCycle);
        formData.append('print_pipeline_registers', printPipelineRegisters);
        // formData.append('print_specific_pipeline_registers', [printSpecificPipelineRegisters, instructionNumber]);  
        formData.append('print_specific_pipeline_registers',printSpecificPipelineRegisters);
        formData.append('data_cache', dataCache);
        formData.append('data_cache_block', dataCacheBlock);
        formData.append('data_associativity', associativityData);
        formData.append('data_ways', waysData);
        formData.append('inst_cache', instCache);
        formData.append('inst_cache_block', instCacheBlock);
        formData.append('inst_associativity', associativityInst);
        formData.append('inst_ways', waysInst);
        formData.append('policy', policy);
        if(instructionNumber != null) formData.append('number',instructionNumber);
        else formData.append('number',0);
        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(
            fetch('http://127.0.0.1:5000/runScripts',{
                method: 'POST',
                body: JSON.stringify('Hello')
            })
            .then(() => {
                console.log('Successfully returned after running both files')
                window.location = 'http://localhost:3000/memory'
            })
            .catch(error => console.log(error))
        )
        .catch(error => console.error(error));
    };
    return (
        <>
            <div className="pt-14 flex flex-col items-center justify-center h-screen text-gray-300">
            <label className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded bg-purple-900">
        Upload File
        <input
          type="file"
          className="hidden"
          accept=".txt,.mc"
          onChange={handleFileInput}
        />
      </label>
      {selectedFile && <p>{selectedFile.name}</p>}
                <div className="pt-12 flex flex-col w-full space-y-2 mb-4 place-items-center justify-items-center">
                    
                    <label className="text-2xl font-bold">Options:</label>
                    
                    <div className="flex items-center space-x-4 pb-2">
                    <input
                        type="checkbox"
                        className="h-6 w-6"
                        checked={pipeliningEnabled}
                        onChange={handlePipeliningEnabled}
                    />
                    <label className="text-lg font-medium">Enable pipelining</label>
                    </div>
                    <div className="flex items-center space-x-4 pb-2">
                    <input
                        type="checkbox"
                        className="h-6 w-6"
                        checked={forwardingEnabled}
                        onChange={handleForwardingEnabled}
                    />
                    <label className="text-lg font-medium">Enable forwarding</label>
                    </div>
                    <div className="flex items-center space-x-4 pb-2">
                    <input
                        type="checkbox"
                        className="h-6 w-6"
                        checked={printRegistersEachCycle}
                        onChange={handlePrintRegistersEachCycle}
                    />
                    <label className="text-lg font-medium">Enable printing registers in each cycle</label>
                    </div>
                    <div className="flex items-center space-x-4 pb-2">
                    <input
                        type="checkbox"
                        className="h-6 w-6"
                        checked={printPipelineRegisters}
                        onChange={handlePrintPipelineRegisters}
                    />
                    <label className="text-lg font-medium">Enable printing pipeline registers</label>
                    </div>
                    <div className="flex items-center space-x-4 pb-2">
                    <input
                        type="checkbox"
                        className="h-6 w-6"
                        checked={printSpecificPipelineRegisters}
                        onChange={handlePrintSpecificPipelineRegisters}
                    />
                    <label className="text-lg font-medium">Enable printing specific pipeline registers</label>
                    {
                        printSpecificPipelineRegisters && (
                            <>
                            <input
                                type="number"
                                id="number-input"
                                value={instructionNumber}
                                onChange={handleInstructionNumber}
                                required
                            />
                            <label className="text-lg font-medium">Enter the number</label>
                            </>
                        )
                    }
                    
                    </div>
                    <div className="grid md:grid-cols-2 pt-5 flex-wrap place-items-center">
                        <div className="pr-10">
                            <label className="text-xl font-bold">Data Cache</label>
                            <div className="flex items-center space-x-4 pb-2">
                            <label className="text-lg font-medium">Cache Size (in Bytes)</label>
                            <input
                                type="number"
                                id="number-input"
                                value={dataCache}
                                className="text-gray-900"
                                onChange={handleDataCache}
                            />
                            </div>
                            <div className="flex items-center space-x-4 pb-2">
                            <label className="text-lg font-medium">Cache block Size (in Bytes)</label>
                            <input
                                type="number"
                                id="number-input"
                                value={dataCacheBlock}
                                className="text-gray-900"
                                onChange={handleDataCacheBlock}
                            />
                            </div>
                            <div className="flex items-center space-x-4 pb-2">
                            <label className="text-lg font-medium">Cache Size (in Bytes)</label>
                            <select
                                className="text-lg font-medium text-gray-900"
                                value={associativityData}
                                onChange={handleassociativityData}
                            >
                                {Object.keys(options).map((option) => (
                                    <option className="text-gray-900" key={option} value={option}>
                                    {options[option]}
                                    </option>
                                ))}
                            </select>
                            </div>
                            <div className="flex items-center space-x-4 pb-2">
                            <label className="text-lg font-medium">Number of Ways:</label>
                            <input
                                type="number"
                                id="number-input"
                                className="text-gray-900"
                                value={waysData}
                                onChange={handleWaysData}
                            />
                            </div>
                        </div>
                        <div className="pl-10">
                            <label className="text-xl font-bold">Information Cache</label>
                            <div className="flex items-center space-x-4 pb-2">
                            <label className="text-lg font-medium">Cache Size (in Bytes)</label>
                            <input
                                type="number"
                                id="number-input"
                                className="text-gray-900"
                                value={instCache}
                                onChange={handleDataCache1}
                            />
                            </div>
                            <div className="flex items-center space-x-4 pb-2">
                            <label className="text-lg font-medium">Cache block Size (in Bytes)</label>
                            <input
                                type="number"
                                id="number-input"
                                className="text-gray-900"
                                value={instCacheBlock}
                                onChange={handleDataCacheBlock1}
                            />
                            </div>
                            <div className="flex items-center space-x-4 pb-2">
                            <label className="text-lg font-medium">Cache Size (in Bytes)</label>
                            <select
                                className="text-lg font-medium text-gray-900"
                                value={associativityInst}
                                onChange={handleassociativityData1}
                            >
                                {Object.keys(options).map((option) => (
                                    <option className="text-gray-900" key={option} value={option}>
                                    {options[option]}
                                    </option>
                                ))}
                            </select>
                            </div>
                            <div className="flex items-center space-x-4 pb-2">
                            <label className="text-lg font-medium">Number of Ways:</label>
                            <input
                                type="number"
                                id="number-input"
                                className="text-gray-900"
                                value={waysInst}
                                onChange={handleWaysData1}
                            />
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center space-x-4 pb-2">
                            <label className="text-lg font-medium">Replacement Policy</label>
                            <select
                                className="text-lg font-medium text-gray-900"
                                value={policy}
                                onChange={handlePolicy}
                            >
                                {Object.keys(options1).map((option) => (
                                    <option className="text-gray-900" key={option} value={option}>
                                    {options1[option]}
                                    </option>
                                ))}
                            </select>
                            </div>
                    <center><button className="w-36 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded bg-purple-900" onClick={handleSubmit}>
                        Submit
                    </button></center>
                </div>
            </div>
        </>
    );
}

export default Input;