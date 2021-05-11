import { GeoJSON } from 'react-leaflet';

import { Stop } from '../stops/Stops';

export type Shape = {
  id: string;
  geometry: GeoJSON.LineString;
};

export type Route = {
  id: string;
  name: string;
  stops: Stop[];
  shapes: Shape[];
  agency: {
    name: string;
  };
};
