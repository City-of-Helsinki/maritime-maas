import { useQuery } from 'react-query';

import { axiosInstance } from '../../common/util/axios';
import { Route } from '../routes/types';

export const useRoute = (id: string, params: string) => {
  return useQuery('route', async () => {
    const route = await axiosInstance.get(`/v1/routes/${id}/?${params}`);
    console.log(route);
    const shapes = await axiosInstance.get(
      `/v1/shapes/?route_id=${route.data.id}`
    );
    return {
      route: route.data,
      shapes: shapes.data,
    };
  });
};

export const useStops = (params: string) => {
  return useQuery('stops', () =>
    axiosInstance.get(`/v1/stops/?${params}`).then((response) => response.data)
  );
};

export const useRoutes = (params: string) => {
  return useQuery('routes', async () => {
    const response = await axiosInstance.get(`/v1/routes/?${params}`);
    await Promise.all(
      response.data.map((route: Route) =>
        axiosInstance
          .get(`/v1/shapes/?route_id=${route.id}`)
          .then((response) => (route.shapes = response.data))
      )
    );
    console.log(response.data);
    return response.data;
  });
};

export const buyTicketsApi = async (params: any) => {
  const reservation = await axiosInstance.post('/v1/bookings/', {
    ...params,
    request_id: 123,
    transaction_id: 123,
  });
  console.log(reservation);
  const confirm = await axiosInstance.post(
    `/v1/bookings/${reservation.data.id}/confirm/`,
    {
      request_id: 123,
      transaction_id: 123,
      locale: params['locale'],
    }
  );
  console.log(confirm);
  return confirm.data;
};

// {
// 	"route_id": "14cd1f76-57a6-5afa-9d88-54df4abad577",
// 	"departure_ids": [
// 		"8f803f51-0db0-56e3-bd01-1e9562896fff", "2669da16-0065-5ae9-bd7e-db0829bc1de0"
// 	],
// 	"tickets": [
// 		{ "ticket_type_id": "ec857693-224e-519b-bdf1-35c61e99c6a7", "customer_type_id": "7bbd6b6c-520a-5951-9015-eec0c388fa2e" }

// 	],
// 	"request_id": "123",
// 	"transaction_id": "456",
// 	"locale": "fi"
// }
