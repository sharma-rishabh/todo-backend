from pact import Verifier

def test_verify_contract_newsletter_api_provider():
    verifier = Verifier(provider='Todo-Provider',
                    provider_base_url="http://0.0.0.0:8000")
    success, logs = verifier.verify_pacts('pacts/TodoConsumer-TodoProvider.json')

    assert success == 0
