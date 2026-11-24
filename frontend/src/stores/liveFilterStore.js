import { defineStore } from 'pinia';

export const useLiveFilterStore = defineStore('liveFilter', {
  state: () => ({
    year: 2026,
    month: 'October',
    site: 'PS01',
    isLoading: false,
    hasData: false,
    docName: null,
    data: {},
  }),

  actions: {
    async setFiltersAndFetch({ year, month, site }) {
      this.year = Number(year);
      this.month = month;
      this.site = site;
      await this.fetchLiveData();
    },

    async fetchLiveData() {
      this.isLoading = true;
      try {
        const url = `/api/method/dashboard.api.get_live_dashboard_data?site=${encodeURIComponent(
          this.site
        )}&month=${encodeURIComponent(this.month)}&year=${encodeURIComponent(this.year)}`;
        const res = await fetch(url);
        const json = await res.json();

        const message = json.message || {};
        if (message.status === 'success' && message.data) {
          this.hasData = true;
          this.docName = message.doc_name;
          this.data = message.data;
        } else {
          this.hasData = false;
          this.docName = null;
          this.data = {};
        }
      } catch (err) {
        console.error('Error fetching live dashboard data:', err);
        this.hasData = false;
        this.docName = null;
        this.data = {};
      } finally {
        this.isLoading = false;
      }
    },
  },

  getters: {
    getDataset: (state) => (key) => {
      return state.data[key] || [];
    },
  },
});

