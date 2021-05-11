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
