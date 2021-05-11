import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import { LatLngTuple } from 'leaflet';

import styles from './map.module.css';

type Props = {
  children: React.ReactElement | null;
};

const Map = ({ children }: Props) => {
  const center: LatLngTuple = [60.152222, 24.956048];

  return (
    <div className={styles.container}>
      <MapContainer
        center={center}
        className={styles.map}
        bounds={[
          [60.17182560116401, 25.025220507762153],
          [60.13050828775804, 24.89656552109463],
        ]}
      >
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {children}
      </MapContainer>
    </div>
  );
};

export default Map;
