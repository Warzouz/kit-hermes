# Accès IA / AI access

Sources officielles :
- https://hermes-agent.nousresearch.com/docs/integrations/providers
- https://hermes-agent.nousresearch.com/docs/integrations/nous-portal

## Français

Vérification documentaire : Hermes v0.22.5. Les offres et conditions changent ;
relisez la documentation et le prix affiché par le fournisseur avant connexion.

| Service | Accès documenté | Attention |
|---|---|---|
| ChatGPT / Codex | OAuth, fournisseur `openai-codex` | Modèles Codex autorisés par le compte ; pas un crédit pour l'API OpenAI |
| Nous Portal | OAuth, fournisseur `nous` | Abonnement Portal et quota propres au service |
| GitHub Copilot | Connexion device OAuth, fournisseur `copilot` | Offre et modèles selon le compte ; un jeton GitHub ordinaire ne suffit pas |
| Anthropic | OAuth Max avec crédits extra usage achetés, ou clé API | Le quota Max inclus n'est pas consommé par Hermes ; Pro ne donne pas cet accès OAuth |
| OpenRouter | Clé API ou OAuth qui établit un accès au compte | Facturation/solde séparés ; OAuth ne signifie pas gratuit |
| OpenAI API, Google Gemini, DeepSeek | Clé API | Un abonnement à leur application grand public n'est pas une clé API |
| Modèle local | Endpoint compatible et modèle avec outils | Installation et ressources à prévoir ; pas de promesse de qualité équivalente |

`hermes -p kit-hermes model` ouvre l'assistant de connexion et choix de modèle.
`hermes -p kit-hermes auth add openai-codex` et
`hermes -p kit-hermes auth add nous` sont les chemins OAuth correspondants.
Pour les autres services, utilisez l'assistant : ne devinez pas un type de jeton.
Ne lisez ni ne copiez les fichiers d'authentification d'une autre installation.
Si la personne n'a aucun accès, présentez les options et les coûts affichés,
puis attendez son choix. Aucun achat ni activation d'usage payant sans accord.

## English

Checked against Hermes v0.22.5 documentation. Check current provider terms and
prices before connecting. ChatGPT/Codex OAuth uses `openai-codex`, not OpenAI API
credits. Nous Portal uses `nous` with its own subscription quota. Copilot uses its
device login and account entitlements, not an ordinary GitHub token. Anthropic
OAuth requires Claude Max plus purchased extra-usage credits; included Max quota
is not used and Pro does not grant this OAuth access. An Anthropic API key is a
separate pay-per-token option. OpenRouter supports API keys or account OAuth,
with separate billing. OpenAI API, Gemini, and DeepSeek API keys are distinct
from consumer chat subscriptions. Local endpoints require compatible tooling and
hardware; equivalent quality is not guaranteed.

Use `hermes -p kit-hermes model` for setup, or the `auth add` commands above for
Codex and Nous. Never ask for secrets in chat or copy another installation's
credential stores. With no access, explain available options and displayed costs,
then wait for a choice. Do not buy or activate paid usage without consent.
