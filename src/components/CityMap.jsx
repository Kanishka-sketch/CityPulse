import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
function CityMap() {
 return <section className="panel map-panel" aria-labelledby="map-title"><div className="panel-heading"><div><span className="eyebrow">JAIPUR AT A GLANCE</span><h2 id="map-title">Where is something unusual happening?</h2></div></div><div className="map-legend" aria-label="Map legend"><span><i className="legend-dot red"/>Anomaly detected</span><span><i className="legend-dot amber"/>Needs attention</span><span><i className="legend-dot green"/>Normal</span></div><div className="map-wrapper"><MapContainer center={[26.9124,75.7873]} zoom={12} scrollWheelZoom={false} className="city-map"><TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/></MapContainer><div className="map-empty"><span>⌖</span><p>Unusual activity will be marked here when information is available.</p></div><div className="map-credit">Map data © OpenStreetMap</div></div></section>;
}
export default CityMap;
