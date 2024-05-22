from django.contrib.auth.decorators import user_passes_test
from .permissions import is_admin
from django.http import HttpResponse
from django.template import loader
import logging
logger = logging.getLogger("django")



# Page acceuil
@user_passes_test(is_admin)
def index(request):
    logger.debug("entrée dans la view 'Index'")
    template = loader.get_template('admin_base/index.html')
    context={}
    logger.warning('le contexte pour la view est vide')

    logger.debug("sortie dans la view 'Index', rendu du tempate...")

    return HttpResponse(template.render(context, request))







