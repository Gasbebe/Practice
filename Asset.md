```c#
    private GameObject contentObj;
    private bool _loading = false;
    private string currentContent = "", previousContent = "";
    private static AssetBundle dummy;
    private static Dictionary<string, AssetBundle> saveBundles = new Dictionary<string, AssetBundle>();


    #region vuforia
    protected override void OnTrackingFound()
    {
        base.OnTrackingFound();
        OnContentStart();
    }


    protected override void OnTrackingLost()
    {
        base.OnTrackingLost();
    }
    #endregion


    #region AssetBundle Method
    //해당 에셋번들이 있는지 판단
    private bool CheckedAssetBundleLoad(string keyValue)
    {
        return saveBundles.ContainsKey(keyValue);
    }

    /// <summary>
    /// 에셋 번들 로드 이미 로드가 되어있으면 키값을 이용해 컨텐츠 생성
    /// 없으면 번들을 로드해서 켄텐츠 생성
    /// </summary>
    /// <param name="content">해당페이지 컨텐츠 이름</param>
    private void OnAssetBunbleLoad(string content)
    {
        if (CheckedAssetBundleLoad(content))
        {
            OnCreateContent();
            return;
        }
        else
        {
            StartCoroutine(LoadStart(content, URL.BaseAssetBundle));
        }
    }

    private void OnAssetAllUnLoad()
    {
        foreach (var _savebundles in saveBundles)
        {
            _savebundles.Value.Unload(true);
        }
        saveBundles.Clear();
    }

    IEnumerator LoadStart(string AssetName, string BundleURL)
    {
        _loading = true;
        BundleURL = BundleURL + AssetName;
        using (UnityWebRequest request = UnityWebRequestAssetBundle.GetAssetBundle(BundleURL, 1, 0))
        {
            request.SendWebRequest();

            while (!request.isDone)
            {
                yield return null;
                var pubIsDone = request.isDone;
            }
            if (request.error != null)
                throw new System.Exception("WWW download had an error:" + request.error);

            var bundle = DownloadHandlerAssetBundle.GetContent(request);
            saveBundles.Add(currentContent, bundle);
        }
        OnCreateContent();
        _loading = false;
    }
    #endregion

    /// <summary>
    /// 해당 페이지의 콘텐츠 로드 여부, 콘텐츠 플레이중인지
    /// 판단하여 해당 페이지의 콘텐츠 실행 및 중지
    /// </summary>
    private void OnContentStart()
    {
        currentContent = mTrackableBehaviour.TrackableName;

        //다른페이지일때
        if (previousContent != currentContent)
        {
            if (!playNar.isContensPlay
                && !_loading)
            {
                if(contentObj != null) Destroy(contentObj);
                previousContent = currentContent;

                //이전 페이지 메모리해제
                OnAssetAllUnLoad();
                OnAssetBunbleLoad(currentContent);
            }
        }
        //같은 페이지를 볼때
        else
        {
            if (!playNar.isContensPlay 
                && !_loading)
            {
                OnCreateContent();
            }
        }
    }

    private void OnCreateContent()
    {
        var bundle = saveBundles[previousContent];
        contentObj = Instantiate(bundle.LoadAsset(previousContent), this.transform) as GameObject;
        this.transform.GetChild(1).localScale = new Vector3(1, 1, 1);
    }
```



