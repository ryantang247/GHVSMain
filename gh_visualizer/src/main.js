import { createApp, h } from 'vue'
// import { DefaultApolloClient } from '@vue/apollo-composable'
import { ApolloClient, InMemoryCache } from '@apollo/client/core'
import { createApolloProvider } from '@vue/apollo-option';
import App from './App.vue'

const cache = new InMemoryCache()

const apolloClient = new ApolloClient({
    cache,
    uri: 'https://api.github.com/graphql',
    headers: {
        Authorization: `Bearer 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`,
    },
})

const apolloProvider = createApolloProvider({
    defaultClient: apolloClient,
});


const app = createApp({

    render: () => h(App),
})
app.use(apolloProvider)
app.mount('#app');