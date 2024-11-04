from mozilla_django_oidc.views import OIDCAuthenticationCallbackView
import logging

logger = logging.getLogger(__name__)

class CustomOIDCAuthenticationCallbackView(OIDCAuthenticationCallbackView):
    def get(self, request, *args, **kwargs):
        logger.debug(f"Received callback with code: {request.GET.get('code')} and state: {request.GET.get('state')}")
        # Call the parent method to handle token exchange
        response = super().get(request, *args, **kwargs)
        # print(dict(request.session))
        # print(dict(request.COOKIES))
        # print(request.session["oidc_states"][request.GET["state"]])
        if "oidc_states" not in request.session:
            logger.error("No oidc_states.")
        if "code" not in request.GET or "state" not in request.GET:
            logger.error("No code/state.")
        state = request.GET.get("state")
        if state not in request.session["oidc_states"]:
            logger.error("No state!")
        print(request.session["oidc_states"])
        if response.status_code == 200:
            logger.debug("Token exchange completed successfully.")
        else:
            logger.error("Token exchange failed.")
            logger.error(f'{response.status_code}, {response.headers}')

        return response