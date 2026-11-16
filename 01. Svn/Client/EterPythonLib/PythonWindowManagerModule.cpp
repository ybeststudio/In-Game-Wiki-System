// PyObject *wndImageSetRenderingRect(PyObject *poSelf, PyObject *poArgs) icinde:
// Ara:
		((UI::CExpandedImageBox*)pWindow)->SetRenderingRect(fLeft, fTop, fRight, fBottom);
	else if (pWindow->IsType(UI::CAniImageBox::Type()))
		((UI::CAniImageBox*)pWindow)->SetRenderingRect(fLeft, fTop, fRight, fBottom);

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM
	else if (pWindow->IsType(UI::CRenderTarget::Type()))
		((UI::CRenderTarget*)pWindow)->SetRenderingRect(fLeft, fTop, fRight, fBottom);
#endif

