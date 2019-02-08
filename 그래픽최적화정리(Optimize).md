# 그래픽스 최적화

#### Draw Call

CPU는 현재 프레임에서 어떤 것을 그려야 할지 결정하고, 오브젝트를 렌더링 하는것을 GPU에 위임합니다. GPU는 CPU의 명령의 따라 렌더링 작업을 수행합니다. 이 과정에서 CPU가 GPU에게 오브젝트를 그리라는 명령을 호출하는게 드로우 콜입니다.

#### Render State

GPU는 그려야 하는 상태 정보를 담는 테이블을 가지고 있습니다 텍스처는 무엇을 사용할지, 쉐이더, 버텍스들은 무엇을 사용할 것인지 등의  상태 정보를 기억하는 것입니다.  이러한 슬롯의 테이블을 렌더 상태라고 표현합니다.



#### Deferred Rendering(디퍼드 렌더링)

디퍼드 렌더링은 많은 수의 실시간 라이팅 즉 동적인 라이트를 비교적 좋은 성능로 처리할 수 있습니다.실시간 라이팅이 많이 쓰이는 오늘날의 게임에서는 적합한 방식이기 때문에 게임에서 널리 쓰이고 있는 렌더링 방식 입니다.

한번에 하나의 버퍼에 레너링 하는 것이 아니라 여러 개의 버퍼에 한꺼번에 렌더링을 하는 멀티 렌더 타겟 기능이 필요합니다

멀티 렌더 타겟을 이용해서 지오메트리 버퍼 혹은 G버퍼라 부르는 여러 개의 버퍼에 불투명, 디퓨즈 스크린 스페이스 노멀, 스페큘러, 스무스니스, 스크린 스페이스 뎁스 등의 정보가 기록 됩니다.



#### Forward Rendering(포워드 렌더링)

포워드 렌더링은  포인트 라이팅, 포워드 쉐이딩 등의 이름으로 불립니다 포워드 라이팅은 전통적인 오브젝트 렌더링 기법입니다.



#### Texture(텍스처)

텍스처는 게임 렌더링에 있어서 필수적인 에셋 중 하나입니다. 텍스처는 오브젝트를 렌더링 할 떄 텍스처 매핑을 통해서 사용됩니다 텍스처 매핑은 컴퓨터 그래픽스 분야에서 가상의 3차워 물체의 표면에 세부적인 질감을 묘사하거나 컬러를 입히는 기법입니다.

텍스퍼는 주로 픽셀 쉐이더 단계에서 사용됩니다. 픽셀 쉐이더에서 텍스처의 값을 샘플링해서 최종 컬러에 반영 시키는 작업을 거치는 것입니다



#### ETC (Ericsson Texture Compression)

텍스처 압축방식



#### UPScale Sampling

화면 해상도를 낮게 렌더링 결과를 현재 화면 해상도에 맞게 늘려 렌더링 하는 방법 이렇게 렌더링을 하게되면 화면이 계산식으로 보이게 된다 (ex : 검은사막 모바일)

```c#
using UnityEngine;
using UnityEngine.UI;

public class UpScaleSampling : MonoBehavior
{
	RenderTexture rt;
	float ratio = 0.5f;
	
	public void CreateRT(float scale)
    {
    	ratio = scale;
    	int width = (int)((float)Screen.width * ratio);
    	int height = (int)((float)Screen.height * ration);
    	
    	rt = new RenderTexture(width, height, 24, RenderTextureFormat.DefaultHDR);
    	rt.Create();
    	GetComponent<Camera>().targetTexture = rt;
    }
}
```



#### 