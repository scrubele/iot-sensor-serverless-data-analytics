Vue.http.headers.common['X-CSRFToken'] = "{{ csrf_token }}";

const API_URL = "http://127.0.0.1:8000";
let vm = new Vue({
  el: '#starting',
  delimiters: ['${','}'],
  data: {
    protectedObjects: [],
    loading: true,  
    currentProtectedObject: {},
    message: null,
    newProtectedObject: { 'name': null, 'description': null,  },
    newRobot:{'name':null, 'detection_algorithm':null, 'price': null},
    search_term: '',
    selectedObject:'',
  },
  mounted: function() {
    this.getProtectedObjects();
  },
  methods: {
    getProtectedObjects: function() {
      let api_url = `${API_URL}/api/protected_objects/`;
      // if(this.search_term!==''||this.search_term!==null) {
      //   api_url = `http://127.0.0.1:8000/api/protectedObject?search=${this.search_term}`
      // }
      this.loading=true;
      this.$http.get(api_url)
          .then((response) => {
            this.protectedObjects = response.data;
            console.log(response.data);
            for (var element in response.data) {
              var id = response.data[element].id;
              vm.getRobotsOfProtectedObject(response.data[element]);
            }
          })
          .catch((err) => {
            this.loading = false;
            console.log("err");
            console.log(err);
          })

    },
    getProtectedObject: function(id) {
      this.loading = true;
      this.$http.get(`${API_URL}/api/protected_objects/${id}/`)
          .then((response) => {
            this.currentProtectedObject = response.data;
            $("#editProtectedObjectModal").modal('show');
            this.loading = false;
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
    addProtectedObject: function() {
      this.loading = true;
      this.$http.post(`${API_URL}/api/protected_objects/`,this.newProtectedObject)
          .then((response) => {
            this.getProtectedObjects();
          })
          .catch((err) => {
            console.log(err);
          })
    },
    updateProtectedObject: function() {
      this.loading = true;
      this.$http.put(`${API_URL}/api/protected_objects/${this.currentProtectedObject.protectedObject_id}/`, this.currentProtectedObject)
          .then((response) => {
            this.loading = false;
            this.currentProtectedObject = response.data;
            this.getProtectedObjects();
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
    deleteProtectedObject: function(id) {
      this.loading = true;
      this.$http.delete(`${API_URL}/api/protected_objects/${id}/`)
          .then((response) => {
            this.loading = false;
            this.getProtectedObjects();
          })
          .catch((err) => {
            this.loading = false;
            console.log(err);
          })
    },
    getRobotsOfProtectedObject: function(object) {
      let id = object.id;
      var pos = this.protectedObjects.indexOf(object);
      let api_url = `${API_URL}/api/protected_objects/${id}/robots/`;
      this.$http.get(api_url)
          .then((response) => {
            // console.log( response.data );
            this.protectedObjects[pos].robots = response.data;
            return response.data;
          })
          .catch((err) => {
            this.loading = false;
            console.log("err");
            console.log(err);
          })
      
    },
    addRobotToProtectedObject: function(id) {
      let api_url = `${API_URL}/api/protected_objects/${id}/robots/`;
      console.log(this.newRobot);
      this.$http.post(api_url,this.newRobot)
          .then((response) => {
            this.getProtectedObjects();
          })
          .catch((err) => {            
            console.log(err);
          })
    },
    selectObject(item) {
      console.log(item);
      this.selectedObject = item;
  },
  }
});