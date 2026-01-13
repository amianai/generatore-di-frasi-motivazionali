const { createApp } = Vue;

createApp({
  data() {
    return {
      moods: [],
      form: {
        mood: "calma",
        seed: "",
        max_tokens: 30,
        n: 3,
        top_k: 25,
        temperature: 1.0,
      },
      output: "",
      info: {
        mood: "-",
        seed: "-",
        n: "-",
        top_k: "-",
        temperature: "-",
        max_tokens: "-",
      },
      loading: false,
    };
  },
  computed: {
    moodDescription() {
      const selected = this.moods.find((mood) => mood.name === this.form.mood);
      return selected ? selected.description : "";
    },
  },
  methods: {
    async fetchMoods() {
      const response = await fetch("/api/moods");
      const data = await response.json();
      this.moods = data.moods || [];
      if (this.moods.length) {
        this.form.mood = this.moods[0].name;
      }
    },
    async generate() {
      this.loading = true;
      try {
        const response = await fetch("/api/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.form),
        });
        const data = await response.json();
        if (!response.ok) {
          this.output = data.detail || "Errore nella generazione";
          return;
        }
        this.output = data.text;
        this.info = data.used;
      } catch (error) {
        this.output = "Errore di rete";
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.fetchMoods();
  },
}).mount("#app");
