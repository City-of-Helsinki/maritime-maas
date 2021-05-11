import axios from 'axios';

import Config from '../../domain/config';

export const axiosInstance = axios.create({
  baseURL: Config.baseUrl,
  headers: {
    authorization: `Bearer ${Config.apiKey}`,
    'Accept-Language': 'fi',
  },
});
