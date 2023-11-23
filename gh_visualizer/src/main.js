import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import draggable from "vuedraggable"
import { loadFonts } from './plugins/webfontloader'
// import {ApolloClient, InMemoryCache} from "@apollo/client";

loadFonts()
// const cache = new InMemoryCache()
// const apolloClient = new ApolloClient({
//     cache,
//     uri: 'https://api.github.com/graphql',
//     headers: {
//         Authorization: `Bearer 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`,
//     },
// })

// const apolloProvider = createApolloProvider({
//     defaultClient: apolloClient,
// });
//
//
// const app = createApp({
//
//     render: () => h(App),
// })

createApp(App)
    .use(vuetify)
    .use(draggable)
    .mount('#app')
