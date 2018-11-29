```c#
    IEnumerator load(string AssetName, string BundleURL)
    {
        _loading = true;
        using (UnityWebRequest request = UnityWebRequestAssetBundle.GetAssetBundle(BundleURL, 1, 0))
        {
            request.SendWebRequest();

            while (!request.isDone)
            {
                yield return null;
                //pubDownloadProgress = request.downloadProgress;
                var pubIsDone = request.isDone;
            }
            if (request.error != null)
                throw new System.Exception("WWW download had an error:" + request.error);
            
            if(bundle == null)
                bundle = DownloadHandlerAssetBundle.GetContent(request);
            //yield return new WaitForSeconds(3);
            if (AssetName == "dino01")
            {
                Instantiate(bundle.LoadAsset("dino01"), this.transform);
                this.transform.GetChild(1).localScale = new Vector3(1, 1, 1);
            }
            else if (AssetName == "dino02")
            {
                Instantiate(bundle.LoadAsset("dino02"), this.transform);
                this.transform.GetChild(1).localScale = new Vector3(1, 1, 1);
            }
            else if (AssetName == "dino03")
            {
                Instantiate(bundle.LoadAsset("dino03"));
                //DefaultTrackableEventHandler.obj.transform.GetChild(1).localScale = new Vector3(1, 1, 1);
            }
            else
               bundle.Unload(false);
        }
```



