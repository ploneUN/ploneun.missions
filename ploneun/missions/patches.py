from logging import getLogger

logger = getLogger('ploneun.missions')

def _patch_redirect():
    # XXX: really ugly patch

    from Products.CMFFormController.Actions.RedirectTo import RedirectTo
    
    if getattr(RedirectTo, '__ploneun_edit_redirect_patched', False):
        return

    logger.info('Patching CMFFormController RedirectTo with support to ' + 
       'redirect File add/edit back to Mission Report')

    from Products.ATContentTypes.interfaces.file import IATFile
    from plone.app.blob.interfaces import IATBlobFile
    from ploneun.missions.content.missionreport import IMissionReport
    from Acquisition import aq_parent

    _getArg = RedirectTo.getArg

    def getArg(self, controller_state):
        url = _getArg(self, controller_state)

        if controller_state.id not in ['atct_edit', 'update_version_on_edit']:
            return url

        context = controller_state.getContext()

        if IATFile.providedBy(context) or IATBlobFile.providedBy(context):
            parent = aq_parent(context)
            if IMissionReport.providedBy(parent):
                return parent.absolute_url()

        return url

    RedirectTo.getArg = getArg
    RedirectTo.__ploneun_edit_redirect_patched = True

_patch_redirect()
