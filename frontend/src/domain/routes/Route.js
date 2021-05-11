import React, { useState, Fragment } from 'react';
import { Marker, Popup, GeoJSON, Polyline, Tooltip } from 'react-leaflet';
import { LatLngExpression } from 'leaflet';
import { format } from 'date-fns';
import { useParams } from 'react-router-dom';

import { useRoute } from '../hooks/api-hooks';
import Map from '../../common/map/Map';
import { Stop } from '../stops/Stops';
import styles from './routes.module.css';
import { Route, Shape } from './types';

const Routeh = () => {
  const [params, setParams] = useState(
    `date=${format(new Date(), 'yyyy-MM-dd')}`
  );
  let { id } = useParams();

  const { data, refetch } = useRoute(id, params);

  if (id != data?.route?.id) return null;

  const drawLine = (stops) => {
    return stops.map((stop) => {
      return [stop.coordinates.latitude, stop.coordinates.longitude];
    });
  };

  if (!data) return null;

  console.log(data.route);

  return (
    <>
      <Map>
        <Fragment key={data?.route?.name + data?.route?.id}>
          {data?.route?.stops?.map((stop) => (
            <Marker
              key={stop.id}
              position={[stop.coordinates.latitude, stop.coordinates.longitude]}
            >
              <Popup>
                <p>{stop.name}</p>
                {/* <ul>
                  {stop.departures.map((d) => (
                    <li>{d.departure_time}</li>
                  ))}
                </ul> */}
              </Popup>
            </Marker>
          ))}
          {data?.shapes.length ? (
            data.shapes.map((shape) => (
              <GeoJSON
                key={shape.id}
                data={shape.geometry}
                pathOptions={{
                  color: getColorForUUID(data.route.id),
                }}
              ></GeoJSON>
            ))
          ) : (
            <Polyline
              positions={drawLine(data?.stops)}
              pathOptions={{ color: 'black' }}
            ></Polyline>
          )}
        </Fragment>
      </Map>
      <h3>{data?.route?.name}</h3>
      <p>{data?.route?.description}</p>
      <h3>Tickets</h3>
      <ul>
        {data?.route?.ticket_types.map((tt) => (
          <li>
            {tt.name}
            <ul>
              {tt.customer_types.map((ct) => (
                <li>{ct.name}</li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
      {/* <table>
        {data?.route?.stops?.map((stop) => (
          <p>{stop.name}</p>
        ))}
      </table> */}
    </>
  );
};

const getColorForUUID = (uuid) => {
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

export default Routeh;
