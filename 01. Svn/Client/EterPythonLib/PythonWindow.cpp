// Ara:
	CRenderTarget::CRenderTarget(PyObject *ppyObject) : CWindow(ppyObject)
	{
		m_dwIndex = -1;

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM



		memset(&rect_ex, 0, sizeof(rect_ex));



#endif


// Ara:
		return true;
	}

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM



	void CRenderTarget::SetRenderingRect(float fLeft, float fTop, float fRight, float fBottom)



	{



		memset(&rect_ex, 0, sizeof(rect_ex));



		float fWidth = float(GetWidth());



		float fHeight = float(GetHeight());







		rect_ex.left = fWidth * fLeft;



		rect_ex.top = fHeight * fTop;



		rect_ex.right = fWidth * fRight;



		rect_ex.bottom = fHeight * fBottom;



	}



#endif


// Bul:



		target->SetRenderingRect(&m_rect);




// Degistir:
#ifdef ENABLE_WIKI_SYSTEM



		RECT rect_real;



		rect_real.left = m_rect.left - rect_ex.left;



		rect_real.top = m_rect.top - rect_ex.top;



		rect_real.right = m_rect.right + rect_ex.right;



		rect_real.bottom = m_rect.bottom + rect_ex.bottom;



		target->SetRenderingRect(&rect_real);



#else



		target->SetRenderingRect(&m_rect);



#endif

