import "./App.css";
import Navbar from "./components/Navbar";
import HealthScore from "./components/HealthScore";
import MetricCard from "./components/MetricCard";
import ActiveInsight from "./components/ActiveInsight";
import ConnectedSignals from "./components/ConnectedSignals";
import CityMap from "./components/CityMap";
import AnomalyList from "./components/AnomalyList";
import HowItWorks from "./components/HowItWorks";
const signals=[{title:"Rain",detail:"Rainfall",icon:"☂",unit:"mm",interpretation:"Rainfall information unavailable"},{title:"Traffic",detail:"Traffic speed",icon:"↗",unit:"km/h",interpretation:"Traffic information unavailable"},{title:"Citizen complaints",detail:"Reports from residents",icon:"▤",unit:"reports",interpretation:"No updates available"},{title:"Air quality",detail:"Fine particles (PM2.5)",icon:"◌",unit:"µg/m³",interpretation:"Air quality unavailable"},{title:"Power",detail:"Outages",icon:"ϟ",unit:"events",interpretation:"Power information unavailable"}];
function App(){return <div className="app"><Navbar/><main><HealthScore/><section className="pulse-card" aria-labelledby="pulse-title"><div className="pulse-icon" aria-hidden="true">◉</div><div><span className="eyebrow">TODAY AT A GLANCE</span><h2 id="pulse-title">Today’s city pulse</h2><p>We’re waiting for current city updates. Once available, this is where you’ll get a quick, plain-language picture of what’s happening in Jaipur.</p></div></section><section className="metrics-section" aria-labelledby="signals-heading"><div className="section-heading"><div><span className="eyebrow">A QUICK LOOK AROUND THE CITY</span><h2 id="signals-heading">What’s happening around Jaipur?</h2></div><span className="data-pending">Updates unavailable</span></div><div className="metrics">{signals.map(signal=><MetricCard key={signal.title}{...signal}/>)}</div></section><div className="dashboard-grid"><ActiveInsight/><CityMap/></div><ConnectedSignals/><AnomalyList/><HowItWorks/></main><footer className="footer-note">CityPulse <span>·</span> Jaipur civic preview</footer></div>}
export default App;
