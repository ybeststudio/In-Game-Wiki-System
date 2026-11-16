// Ara:
			CRenderTarget(PyObject *ppyObject);
			virtual ~CRenderTarget();
			bool SetRenderTarget(int index);

// Altina ekle:
#ifdef ENABLE_WIKI_SYSTEM

			void SetRenderingRect(float fLeft, float fTop, float fRight, float fBottom);

			RECT rect_ex;

#endif

