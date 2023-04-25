import React, {useCallback} from 'react'
import './App.css';
import MemoryScreen from './Components/MemoryScreen.js'
import RegisterScreen from './Components/RegisterScreen.js';
import DataHazardScreen from './Components/DataHazardScreen';
import Simulator from './Components/Simulator.js'
import HitScreen from './Components/HitScreen';
import DCacheScreen from './Components/DCacheScreen';
import ICacheScreen from './Components/ICacheScreen';
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import Input from './Components/input.js'
import Particles from "react-particles";
import { loadFull } from "tsparticles";

const App = () => {
  const particlesInit = useCallback(async engine => {
      console.log(engine);
      // you can initiate the tsParticles instance (engine) here, adding custom shapes or presets
      // this loads the tsparticles package bundle, it's the easiest method for getting everything ready
      // starting from v2 you can add only the features you need reducing the bundle size
      await loadFull(engine);
  }, []);

  const particlesLoaded = useCallback(async container => {
      await console.log(container);
  }, []);
  return (
    <>
    <div className='App'>
      <div id="particles-container">
    <Particles
            id="tsparticles"
            init={particlesInit}
            loaded={particlesLoaded}
            options={{
                background: {
                    color: {
                        value: "#3d285c",
                    },
                },
                fpsLimit: 120,
                interactivity: {
                    events: {
                        onClick: {
                            enable: true,
                            mode: "push",
                        },
                        onHover: {
                            enable: true,
                            mode: "repulse",
                        },
                        resize: true,
                    },
                    modes: {
                        push: {
                            quantity: 4,
                        },
                        repulse: {
                            distance: 200,
                            duration: 0.4,
                        },
                    },
                },
                particles: {
                    color: {
                        value: "#ffffff",
                    },
                    links: {
                        color: "#ffffff",
                        distance: 150,
                        enable: true,
                        opacity: 0.5,
                        width: 1,
                    },
                    collisions: {
                        enable: true,
                    },
                    move: {
                        direction: "none",
                        enable: true,
                        outModes: {
                            default: "bounce",
                        },
                        random: false,
                        speed: 3,
                        straight: false,
                    },
                    number: {
                        density: {
                            enable: true,
                            area: 800,
                        },
                        value: 80,
                    },
                    opacity: {
                        value: 0.5,
                    },
                    shape: {
                        type: "circle",
                    },
                    size: {
                        value: { min: 1, max: 5 },
                    },
                },
                detectRetina: true,
            }}
        />
      </div>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Input />} />
        <Route path='/memory' element={<MemoryScreen />} />
        <Route path='/register' element={<RegisterScreen />} />
        <Route path='/dataHazard' element={<DataHazardScreen />} />
        <Route path='/simulator' element={<Simulator />} />
        <Route path='/Hits' element={<HitScreen />}/>
        <Route path='/dataCache' element={<DCacheScreen/>} />
        <Route path='/instCache' element={<ICacheScreen/>} />
      </Routes>
      </BrowserRouter>
    </div>
    </>
  )
}

export default App
