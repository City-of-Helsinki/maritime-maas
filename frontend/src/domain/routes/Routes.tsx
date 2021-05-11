import React, { useState, Fragment } from 'react';
import { Marker, Popup, GeoJSON, Polyline, Tooltip } from 'react-leaflet';
import { LatLngExpression } from 'leaflet';
import { useHistory } from 'react-router-dom';

import { useRoutes } from '../hooks/api-hooks';
import Map from '../../common/map/Map';
import { Stop } from '../stops/Stops';
import styles from './routes.module.css';
import { Route, Shape } from './types';

const Routes = () => {
  const history = useHistory();
  const [params, setParams] = useState<string>('');
  const { data, refetch } = useRoutes(params);

  const search = (e: React.SyntheticEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const params = new URLSearchParams(formData as URLSearchParams).toString();
    setParams(params);
    setTimeout(() => {
      refetch();
    }, 200);
  };

  const drawLine = (stops: Stop[]): LatLngExpression[] => {
    return stops.map((stop: Stop) => {
      return [stop.coordinates.latitude, stop.coordinates.longitude];
    });
  };

  const getColorForUUID = (uuid: string): string => {
    console.log(uuid);
    return (
      '#' +
      (
        uuid
          .split('')
          .map((s) => s.charCodeAt(0))
          .reduce((a, b) => a * 777 + b, 0) % 0xffffff
      )
        .toString(16)
        .padStart(6, '0')
    );
  };

  console.log(data);

  return (
    <>
      {/* <h1>Routes</h1>
      <form onSubmit={search} className={styles.form}>
        <label htmlFor="stop_id">Stop id</label>
        <input name="stop_id" className={styles.input} />
        <button type="submit">Search</button>
      </form> */}
      <Map>
        {data?.map((route: Route) => (
          <Fragment key={route.name + route.id}>
            {route?.stops?.map((stop: Stop) => (
              <Marker
                key={stop.id}
                position={[
                  stop.coordinates.latitude,
                  stop.coordinates.longitude,
                ]}
              >
                <Popup>
                  {/* <p>{stop.id}</p> */}
                  <h3>{stop.name}</h3>
                  {/* <p>
                    <a href={`/routes/${route.id}`}>{route.name}</a>
                  </p> */}
                </Popup>
              </Marker>
            ))}
            {route?.shapes.length ? (
              route.shapes.map((shape: Shape) => (
                <GeoJSON
                  key={shape.id}
                  data={shape.geometry}
                  // onclick={alert('UGH')}
                  onEachFeature={(feature, layer) => {
                    layer.on('click', function (e) {
                      history.push(`/routes/${route.id}`);
                    });
                  }}
                  pathOptions={{
                    color: getColorForUUID(route?.agency?.name),
                  }}
                >
                  <Tooltip sticky>{route.name}</Tooltip>
                </GeoJSON>
              ))
            ) : (
              <Polyline
                positions={drawLine(route?.stops)}
                pathOptions={{ color: 'black' }}
              >
                <Tooltip>{route.name}</Tooltip>
              </Polyline>
            )}
          </Fragment>
        ))}
      </Map>
    </>
  );
};

export default Routes;
