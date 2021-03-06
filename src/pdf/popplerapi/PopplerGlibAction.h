/*
 * Xournal++
 *
 * PDF Action Abstraction Interface
 *
 * @author Xournal++ Team
 * https://github.com/xournalpp/xournalpp
 *
 * @license GNU GPLv2 or later
 */

#pragma once

#include <string>
#include <vector>

#include <poppler.h>

#include "model/LinkDestination.h"
#include "pdf/base/XojPdfAction.h"


class LinkDestination;


class PopplerGlibAction: public XojPdfAction {
public:
    PopplerGlibAction(PopplerAction* action, PopplerDocument* document);
    virtual ~PopplerGlibAction();

public:
    virtual XojLinkDest* getDestination();
    virtual std::string getTitle();

private:
    void linkFromDest(LinkDestination* link, PopplerDest* pDest);

private:
    PopplerAction* action;
    PopplerDocument* document;
};
