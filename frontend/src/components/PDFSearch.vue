<template>
  <div class="pdf-search">
    <b-form-input v-model="searchTerm" placeholder="Enter your search term"></b-form-input>
    <a
      @click.prevent.stop="searchForKeyword"
      class="icon"
      :disabled="isDisabled"
      style="float: right"
    >
      <PrintIcon />
    </a>
  </div>
</template>

<script>
import PrintIcon from "../assets/icon-search.svg";
import axios from "axios";

export default {
  name: "PDFSearch",

  data() {
    return {
      searchTerm: "",
      resCache: null
    };
  },

  components: {
    PrintIcon
  },

  props: {
    scale: {
      type: Number
    },
    increment: {
      type: Number,
      default: 0.25
    }
  },

  computed: {
    isDisabled() {
      return !this.scale;
    }
  },

  methods: {
    async searchForKeyword() {
      if (this.searchTerm != "") {
        const c = document.getElementsByTagName("canvas");
        const width = c[0].width;
        const height = c[0].height;

        //Clearing
        if (this.resCache != null) {
          this.clearResults();
        }

        const bodyFormData = new FormData();
        bodyFormData.set("width", width);
        bodyFormData.set("height", height);
        bodyFormData.set("q", this.searchTerm);

        let res = await axios.post(
          "http://localhost:5000/document/search",
          bodyFormData,
          {
            headers: { "Content-Type": "multipart/form-data" },
            timeout: 180000
          }
        );
        if (res.data.length > 0) {
          for (const obj of res.data) {
            const page = obj["page"] - 1;
            const ctx = c[page].getContext("2d");
            ctx.globalCompositeOperation = "source-over";
            ctx.beginPath();
            ctx.fillStyle = "#FF0000";
            ctx.globalAlpha = 0.3;
            ctx.fillRect(
              obj["x1"],
              obj["y1"],
              obj["x2"] - obj["x1"],
              obj["y2"] - obj["y1"]
            );
          }
          this.resCache = res.data;
        } else {
          alert(
            "Unfortunately we could not find the word you were searching for"
          );
        }
      } else {
        alert("Please insert a search term first");
      }
    },
    clearResults() {
      for (const obj of this.resCache) {
        const c = document.getElementsByTagName("canvas");
        const page = obj["page"] - 1;
        const ctx = c[page].getContext("2d");
        ctx.globalCompositeOperation = "overlay";
        ctx.beginPath();
        ctx.fillStyle = "#00FFFF";
        ctx.globalAlpha = 1;
        ctx.fillRect(
          obj["x1"],
          obj["y1"],
          obj["x2"] - obj["x1"],
          obj["y2"] - obj["y1"]
        );
      }
    }
  }
};
</script>

<style>
.pdf-search a {
  float: left;
  cursor: pointer;
  display: block;
  border: 1px #333 solid;
  background: white;
  color: #333;
  font-weight: bold;
  line-height: 1.5em;
  width: 1.5em;
  height: 1.5em;
  font-size: 1.5em;
}
</style>
