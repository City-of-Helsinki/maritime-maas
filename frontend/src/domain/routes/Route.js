import React, { useState, Fragment } from 'react';
import { Marker, Popup, GeoJSON, Polyline, Tooltip } from 'react-leaflet';
import { LatLngExpression } from 'leaflet';
import { format } from 'date-fns';
import { useParams } from 'react-router-dom';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

import { useRoute, buyTicketsApi } from '../hooks/api-hooks';
import Map from '../../common/map/Map';
import { Stop } from '../stops/Stops';
import styles from './routes.module.css';
import { Route, Shape } from './types';

const Ticket = (props) => (
  <div
    className="ticket"
    style={{
      maxWidth: '400px',
      margin: '20px auto',
      border: '1px solid #000000',
      padding: '15px',
    }}
  >
    <div
      className="agency"
      style={{
        display: 'flex',
        maxHeight: '150px',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <img style={{ maxHeight: '70px' }} src={props.ticket.agency.logo_url} />
      <div style={{ flex: '100%' }}>
        <h3 style={{ textAlign: 'center' }}>{props.ticket.agency.name}</h3>
      </div>
    </div>
    <hr />
    <div className="routeHeader">
      <h3>{props.ticket.route.name}</h3>
      <h4>
        {props.ticket.ticket_type.name} - {props.ticket.customer_type.name}
      </h4>
      <h4>
        {props.ticket.price.amount_total} {props.ticket.price.currency} (VAT{' '}
        {props.ticket.price.vat_percentage})
      </h4>
    </div>
    <img
      style={{ width: '200px', marginBottom: '20px' }}
      src={props.ticket.qr_code}
    />
    <div style={{ display: 'flex', fontSize: '90%' }}>
      {props.ticket.route.legs.map((l, i) => {
        const divider =
          i > 0 ? (
            <div
              style={{
                borderLeft: '4px solid black',
                height: 'inherit',
                minHeight: '100%',
                width: '6px',
              }}
            />
          ) : null;
        return (
          <>
            {divider}
            <table style={{ flex: '50%' }}>
              {l.stops.map((s) => {
                return (
                  <tr>
                    <td>{format(new Date(s.stop_time), 'hh:mm')}</td>
                    <td>{s.name}</td>
                  </tr>
                );
              })}
            </table>
          </>
        );
      })}
    </div>
    <h5>Lipun kuvaus</h5>
    <p>{props.ticket.ticket_type.description}</p>
    {props.ticket.ticket_type.instructions && (
      <>
        <h5>Lipun ohjeet</h5>
        <p>{props.ticket.ticket_type.intructions}</p>
      </>
    )}

    <h5>Asiakasryhmän kuvaus</h5>
    <p>{props.ticket.customer_type.description}</p>
  </div>
);

const Routeh = () => {
  const [travelDate, setTravelDate] = useState(new Date());
  const [params, setParams] = useState(
    `date=${format(travelDate, 'yyyy-MM-dd')}`
  );
  const [booking, setBooking] = useState({});
  const [tickets, setTickets] = useState({});
  const [departures, setDepartures] = useState([]);
  console.log(departures);
  const [selectDepartures, setSelectDepartures] = useState(false);

  let { id } = useParams();
  const { data, refetch } = useRoute(id, params);
  const legCount = [
    ...new Set(
      data?.route?.stops?.map((s) => s.departures.map((d) => d.block_id)).flat()
    ),
  ].length;

  if (id != data?.route?.id) return null;

  const drawLine = (stops) => {
    return stops.map((stop) => {
      return [stop.coordinates.latitude, stop.coordinates.longitude];
    });
  };

  if (Object.keys(booking).length > 0) {
    return (
      <div>
        {booking.tickets.map((t) => (
          <Ticket ticket={t} />
        ))}
      </div>
    );
  }

  if (!data) return null;

  const dropChange = (e) => {
    const split = e.target.value.split('_');
    e.preventDefault();
    setTickets({
      ...tickets,
      [`${split[0]}_${split[1]}`]: parseInt(split[2]),
    });
  };

  const buyTickets = async (e) => {
    const ticketArray = Object.keys(tickets)
      .map((k) => {
        // tickets[k]
        return [...Array(tickets[k])].map((a) => {
          const split = k.split('_');
          return {
            ticket_type_id: split[0],
            customer_type_id: split[1],
          };
        });
      })
      .flat();
    const params = {
      route_id: data.route.id,
      tickets: ticketArray,
    };
    let book = await buyTicketsApi(params);
    const ticketData = [
      {
        id: '5d1864c8-7996-45ec-8823-914412c00ca2',
        agency: {
          name: 'Suomen saaristokuljetus Oy',
          logo_url: 'https://kauppa.visitvallisaari.fi/img/logo.png',
        },
        customer_type: {
          description: 'Aikuiset',
          name: 'Aikuiset',
        },
        locale: 'fi',
        maas_operator_id: 'maasmies',
        price: {
          amount_excluding_vat: '6.85',
          amount_total: '8.49',
          currency: 'EUR',
          vat_amount: '1.64',
          vat_percentage: '24',
        },
        qr_code:
          'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAHAklEQVR4nO3YwXYrOQhF0fz/T1fP/drEIlBCrn3W8kyiLoiTQX4uAG/52R0AmAxBgACCAAEEAQIIAgQQBAggCBBAECCAIEAAQYAAggABBAECUoL8/Pwc8avK3013/mnznJY/fJvUpQHN3vmg3ZyykNPy3PGOBGkabMU8q/JPm+e0/OHbpC4NaPbOB+3mlIWclueOdyRI02Ar5lmVf9o8p+UP3yZ1aUCzdz5oN6cs5LQ8d7xjqSC7mJbnHd05d4k/bf4EGZ7nHQS5B4IMz/MOgtwDQYbneQdB7oEgw/O8gyD3QJDhed5BkHs4TpDVh6uqX3W+u69pC7zr/K59iCAIQcacJ8iQgRCEIJ9CEIKMOU+QIQMhCEE+hSAEGXOeIEMGMu273XPrFvP0fQh7S106fCDTvts9N4IQhCAESecJe0tdOnwg077bPTeCEIQgBEnnCXtLXTp8INO+2z03ghBk1OJ156yCIB/0lrp0+EAIUlv/9H0Ie0tdOnwgBKmtf/o+hL2lLh0+EILU1j99H8LeUpcOHwhBauufvg9hb6lLhw+EILX1T9+HsLfUpeaH25Wnu86uhT9pISsgSFMeghDkn1q7A1RAkNx3CfJBrd0BKiBI7rsE+aDW7gAVECT3XYJ8UGt3gAoIkvsuQT6oVRlg2q9qgM7nzk/7ZSCI823np/0yEMT5tvPTfhkI4nzb+Wm/DARxvu38tF8Ggjjfdn7aL8O+/8UNpHuRqvKctGCn88yu30AQgrzyzK7fQBCCvPLMrt9AEIK88syu30AQgrzyzK7fQBCCvDLy37xVearOV7FrDlXffVrO6yIIQQgSZ01dIkgKgpyV87oIQhCCxFlTlwiSgiBn5bwughCEIHHW1K3VjxQ12D2oaeJ05+yec/cfhNU8qVplqaKPECSEIAQhSABBCEKQAIIQhCABBCEIQQII8mWCVA2ECLWLPe38LgErIQhB2s4ThCBLEIQgBAkgCEEIEkAQghAkgCAPEeRtsWGNdw/wW/8gdPe1611StcpSJYIRhCAEIQhBCJILRhCCEIQgBCFILhhBCEKQGxZjl1CnL173oq6yS6gwU2kxghDkDxCEIAQJIAhBCBJAEIIQJIAgBCFIwNcIsmvhp4lwep5pdarqVwpFkMEL0J1nWp2q+gQ5dCGn5ZlWp6o+QQ5dyGl5ptWpqk+QQxdyWp5pdarqE+TQhZyWZ1qdqvpjBek+P+0hps2nu99TBCQIQQhCEIJUna/qlyCfXiIIQQgSXCIIQQgSXCIIQQgSXBo2wKr8u+rvXICT83fP4boIMqI+QQjSWqcq/676BCFIa52q/LvqE4QgrXWq8u+qTxCCtNapyr+rPkEeIsjq+W7Rqti1qFVM+8N1yrtfF0H+1C9BCFISjCB7IUgegvyhX4IQpCQYQfZCkDwE+UO/BCHIWrFhjXeLWZX/W/N0f5cgBDk6D0FeixEklf9b8xDktRhBUvm/NQ9BXosRJJX/W/MQ5LUYQVL5vzXPYwXZ9XBVdaoeYtdi37EYFUzbkwwEIUgb0/YkA0EI0sa0PclAEIK0MW1PMhCEIG1M25MMBCFIG9P2JMMtX5m2eN1UCbt6ftcfim4IMvyBViFILQQZ/kCrEKQWggx/oFUIUgtBhj/QKgSphSDDH2gVgtTyNYJ0L8ZqnWm/qvynz6F7npUQZMCDEoQgJedX60z7VeU/fQ4EIQhBCPI/xQhCkAHzrIQgAx6UIA8R5BR2LfwupuU/SSiCEOTP56vyEGQIBCHIx1nLuj4IghDk46xlXR8EQQjycdayrg+CIAT5OOtJDXYPZHfeu4WqylN1vvu7GQgyuK9uCPI7BBncVzcE+R2CDO6rG4L8DkEG99UNQX6HIIP76oYgv1MqyC66BenOuUv8qvNVeablvC6CtNRZrU8QgrRCkNq+ps1hV87rIkhLndX6BCFIKwSp7WvaHHblvC6CtNRZrU+QhwvSvRi7HrT7/DShduXcNYfrIsit/a6eJ0htngwEubHf1fMEqc2TgSA39rt6niC1eTIQ5MZ+V88TpDZPBoLc2O/qeYLU5snwSEF2LdLp9U/vKwNBDnxoguTqZyDIgQ9NkFz9DAQ58KEJkqufgSAHPjRBcvUzEOTAhyZIrn4GgjTkr/ruNKb9Ier+7nURhCALEOTmwAQhyOTvXhdBCLIAQW4OTBCCTP7udRGEIAsQpClwN6c83K783X+gpvVVCUEIQpCoh9QlgmytQ5Dc+QwEIQhBoh5SlwiytQ5BcuczEIQgBIl6SF0qGnj3bzX/LqYt8K75THxHghCEIFGm1KUBy08QghCEIAQhCEEIEuepOp/KlLo0YPkJQpCxggBPgSBAAEGAAIIAAQQBAggCBBAECCAIEEAQIIAgQABBgACCAAEEAQL+A0h7mXOeq/H0AAAAAElFTkSuQmCC',
        route: {
          name: 'Kauppatori - Vallisaari',
          description:
            'Matka Kauppatorilta Vallisaareen ja takaisin. Lippuun sisältyy rajaton ajelu Vallisaaren rengasreitillä',
          legs: [
            {
              stops: [
                {
                  location: {
                    lat: 60.1665471,
                    lon: 24.9538016,
                  },
                  name: 'Kauppatori Lyypekinlaituri',
                  stop_time: '2021-05-01T05:00:00Z',
                },
                {
                  location: {
                    lat: 60.1405804,
                    lon: 25.007042,
                  },
                  name: 'Vallisaari tulolaituri',
                  stop_time: '2021-05-01T05:20:00Z',
                },
              ],
            },
            {
              stops: [
                {
                  location: {
                    lat: 60.1376346,
                    lon: 25.0098517,
                  },
                  name: 'Vallisaari lähtölaituri',
                  stop_time: '2021-05-01T06:25:00Z',
                },
                {
                  location: {
                    lat: 60.1665471,
                    lon: 24.9538016,
                  },
                  name: 'Kauppatori Lyypekinlaituri',
                  stop_time: '2021-05-01T06:45:00Z',
                },
              ],
            },
          ],
        },
        terms_url: '',
        departures: [
          {
            from: 'Kauppatori Lyypekinlaituri',
            to: 'Vallisaari tulolaituri',
            depart_at: '2021-05-11T14:42:47.712273Z',
          },
        ],
        schema_version: 2,
        ticket_type: {
          name: 'Menu-Paluu',
          description: 'Menu-Paluu',
          instructions: '',
        },
        validity: {
          starts_at: '2021-05-11T13:42:47.712273Z',
        },
      },
    ];
    setBooking({ ...book, tickets: ticketData });
  };

  // 	"route_id": "14cd1f76-57a6-5afa-9d88-54df4abad577",
  // 	"departure_ids": [
  // 		"8f803f51-0db0-56e3-bd01-1e9562896fff", "2669da16-0065-5ae9-bd7e-db0829bc1de0"
  // 	],
  // 	"tickets": [
  // 		{ "ticket_type_id": "ec857693-224e-519b-bdf1-35c61e99c6a7", "customer_type_id": "7bbd6b6c-520a-5951-9015-eec0c388fa2e" }

  // 	],
  const deps = selectDepartures
    ? data.route.stops
        .map((s) =>
          s.departures
            .filter((d) => d.direction_id === departures.length)
            .map((d) => {
              return { ...d, stop_name: s.name };
            })
        )
        .flat()
        .sort((a, b) => a.stop_sequence - b.stop_sequence)
        .reduce(function (r, a) {
          r[a.id] = r[a.id] || [];
          r[a.id].push(a);
          return r;
        }, Object.create(null))
    : null;

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
                  color: getColorForUUID(data.route.agency.name),
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
      {!selectDepartures &&
        data?.route?.ticket_types.map((tt) => (
          <div className="tickettype">
            <h3>Liput</h3>
            <h4>{tt.name}</h4>
            <table>
              {tt.customer_types.map((ct) => (
                <tr>
                  <td>
                    <select onChange={dropChange}>
                      <option default value={`${tt.id}_${ct.id}_0`}>
                        0
                      </option>
                      <option value={`${tt.id}_${ct.id}_1`}>1</option>
                      <option value={`${tt.id}_${ct.id}_2`}>2</option>
                      <option value={`${tt.id}_${ct.id}_3`}>3</option>
                      <option value={`${tt.id}_${ct.id}_4`}>4</option>
                      <option value={`${tt.id}_${ct.id}_5`}>5</option>
                    </select>
                  </td>
                  <td>{ct.name}</td>
                  <td>{ct.description}</td>
                  <td>
                    {ct.price} {ct.currency_type}
                  </td>
                </tr>
              ))}
            </table>
          </div>
        ))}
      {selectDepartures && departures.length < legCount && (
        <div style={{ zIndex: '1000' }}>
          <h3>
            Valitse lähtö {departures.length + 1}/{legCount}
          </h3>
          <DatePicker
            popperPlacement="bottom"
            selected={travelDate}
            onChange={(date) => {
              setTravelDate(date);
              setParams(`date=${format(date, 'yyyy-MM-dd')}`);
              refetch();
            }}
          />
          {!!deps && (
            <div style={{ marginTop: '30px' }}>
              <table style={{ minWidth: '500px' }}>
                <tr>
                  {Object.values(deps)[0].map((d) => (
                    <th style={{ padding: '15px' }}>{d.stop_name}</th>
                  ))}
                  <th></th>
                </tr>
                {Object.values(deps)
                  .sort((a, b) => a[0].departure_time > b[0].departure_time)
                  .map((d) => (
                    <tr>
                      {d.map((s) => (
                        <td style={{ textAlign: 'center' }}>
                          {format(new Date(s.departure_time), 'HH:mm')}
                        </td>
                      ))}
                      <td>
                        <button
                          onClick={() => {
                            setDepartures([...departures, d]);
                          }}
                        >
                          Valitse
                        </button>
                      </td>
                    </tr>
                  ))}
              </table>
            </div>
          )}
        </div>
      )}
      {data?.route?.capacity_sales < 2 ||
        (departures.length == legCount && (
          <button className="button" onClick={buyTickets}>
            Osta liput
          </button>
        ))}
      {!selectDepartures &&
        data?.route?.capacity_sales > 1 &&
        departures.length < legCount && (
          <button
            className="button"
            onClick={() => {
              setSelectDepartures(true);
            }}
          >
            Valitse lähdöt
          </button>
        )}

      {/* <table>
        {data?.route?.stops?.map((stop) => (
          <p>{stop.name}</p>
        ))}
      </table> */}
    </>
  );
};

const getColorForUUID = (uuid) => {
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
