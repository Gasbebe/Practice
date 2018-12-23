메쉬 클래스에서

모든 정점은 하나의 배열의 저장되어 있다.

전체 tris 정수들로 이루어진 하나의 긴 베열에 저장된다 이배열은 3개마다 하나의 삼각형으로 그룹하 되어 있다, 0,1,2는 첫번째 삼각형, 3,4,5는 두번째 삼각형으로 이루어지는 형식이다



# 1. Quad Generator

```c#
namespace ProceduralModeling {

	public class Quad : ProceduralModelingBase {

		[SerializeField, Range(0.1f, 10f)] protected float size = 1f;

		protected override Mesh Build() {
			var mesh = new Mesh();

			//quad 크기
			var hsize = size * 0.5f; 

			// Quad 정점 좌표 정의
			var vertices = new Vector3[] {
				new Vector3(-hsize,  hsize, 0f), // 0  왼쪽 상단
				new Vector3( hsize,  hsize, 0f), // 1  오른쪽 상단
				new Vector3( hsize, -hsize, 0f), // 2  오르쪽 하단
				new Vector3(-hsize, -hsize, 0f)  // 3  왼쪽 하단
			};

			// Quad의 uv좌표
			var uv = new Vector2[] {
				new Vector2(0f, 0f), // 0번 정점의 uv좌표
				new Vector2(1f, 0f), // 1번 정점의 uv좌표
				new Vector2(1f, 1f), // 2번 정점의 uv좌표
				new Vector2(0f, 1f)  // 3번 정점의 uv좌표
			};

			// Quad의 법선 데이터
			var normals = new Vector3[] {
				new Vector3(0f, 0f, -1f), // 0번 정점의 법선
				new Vector3(0f, 0f, -1f), // 1번 정점의 법선
				new Vector3(0f, 0f, -1f), // 2번 정점의 법선
				new Vector3(0f, 0f, -1f)  // 3번 정점의 법선
			};

			//Quad의 면데이터 네 개의 버텍스로 이루어진 두 삼각형에 필요한 index를
            //삼각형 순서댈로 2개씩 나라히 놓는다
			var triangles = new int[] {
				0, 1, 2, // 1번 삼각형
				2, 3, 0  // 2번 삼각형
			};

			mesh.vertices = vertices;
			mesh.uv = uv;
			mesh.normals = normals;
			mesh.triangles = triangles;

			//만들어지 메쉬의 경계영역(bounds)을 계산한다 (culling에 필요)
			mesh.RecalculateBounds();

			return mesh;
		}

	}

}
```



# 2. Plane Generator

```c#
namespace ProceduralModeling {

	public class Plane : ProceduralModelingBase {

		// Plane 너비(widthSegments) 높이(heightSegments) 정점의 갯수
		[SerializeField, Range(2, 30)] protected int widthSegments = 8, heightSegments = 8;

		// Plane 크기
		[SerializeField, Range(0.1f, 10f)] protected float width = 1f, height = 1f;

		protected override Mesh Build() {
			var mesh = new Mesh();

			var vertices = new List<Vector3>();
			var uv = new List<Vector2>();
			var normals = new List<Vector3>();

			//격자상에 정점을 배열할 위치의 비율(00. ~ 1.0)을 산출하기 위한 행열수의 역수
			var winv = 1f / (widthSegments - 1);
			var hinv = 1f / (heightSegments - 1);

			for(int y = 0; y < heightSegments; y++) {
				//행의 위치 비율 (0.0 ~ 1.0)
				var ry = y * hinv;

				for(int x = 0; x < widthSegments; x++) {
					//열의 위치 비율(0.0 ~ 1.0)
					var rx = x * winv;

					vertices.Add(new Vector3(
						(rx - 0.5f) * width, 
						0f,
						(0.5f - ry) * height
					));
                    //정점의 갯수 비율에 따른 uv좌표 설정
					uv.Add(new Vector2(rx, ry));
                    //법선 방향 설정
					normals.Add(new Vector3(0f, 1f, 0f));
				}
			}

			var triangles = new List<int>();
			//너비와 높이따른 삼각형 갯수 계산  기본적으론 2개의 삼각형 추가
			for(int y = 0; y < heightSegments - 1; y++) {
				for(int x = 0; x < widthSegments - 1; x++) {
					int index = y * widthSegments + x;
					var a = index;
					var b = index + 1;
					var c = index + 1 + widthSegments;
					var d = index + widthSegments;
					
                    //첫번째 삼각형
					triangles.Add(a);
					triangles.Add(b);
					triangles.Add(c);
					
                    //두번째 삼각형
					triangles.Add(c);
					triangles.Add(d);
					triangles.Add(a);
				}
			}

			mesh.vertices = vertices.ToArray();
			mesh.uv = uv.ToArray();
			mesh.normals = normals.ToArray();
			mesh.triangles = triangles.ToArray();

			mesh.RecalculateBounds();

			return mesh;
		}

	}

}
```

Geometry Shader(Primitive Shader)

Geometry Shader는 gpu상에서 동적으로 프리미티브(primitives, 메쉬를 구성하는 기본 도형)

의 변환,생성, 삭제 등이 가능한 프로그래머블 쉐이더 중 하나입니다.

지금 까지는 프리미티브를 변환하거나 동적으로 메쉬의 형태를 변화시키려 할 때는 cpu상에서 먼저 처리를 하고 gpu로 넘기거나 또는 미리 정점 데이터에 메타 정보를 넣어놓고 Vertex Shader로 변형하는 등의 작업이 필요했습니다. 하지만 Vertex Shader에서는 쉐이더상에서 현제 처리하는 정점에 관한 정보를 얻을수 없고 또한 처리중인 정점을 기준으로 새로운 정점을 만들거나 역으로 삭제하는 등의 작업을 할 수 없는 큰 제약이 있습니다. 만약 cpu상에서 먼저 처리한고 gpu로 넘긴다면 많은 경우 실시간으로 계산하기에는 지나치게 시간이 길어져 현실적이지 않습니다 이처럼 실시간으로 메쉬의 형상을 변화시키는것은 지금까지 몇 가지 문제가 있었습니다.

이러한 문제를 해결하고 쉐이더의 제야을 완화해 gpu상에서 메쉬를 좀 더 자유롭게 변환처리를 할 수 있도록 dx10이나  openGL3.2 부터 추가된 기능입니다.

렌더링 파이프라인

버텍스 쉐이더 다음,  프래그멘트 쉐이더,  래스터라이즈 처리전에 위치합니다

보통 Vertex Shader의 입력정보는 정점단위로 되어 있으며 이들 정점에 대한 변환처리를
합니다. 하지만 GeometrZ Shader로의 입력정보는 유저에 따라 정의된 입력용의 프리미티
브 단위가 되겠습니다.
실제 샘플 프로그램을 통해 후술하겠지만, GeometrZ Shader에서는 Vertex Shader에서
처리한 정점 정보들을 입력에 사용된 프리미티브 형을 기준으로 나누어 입력받을 수 있습
니다. 예를 들어 입력된 프리미티브 형이 triangle이라면 3개의 정점 정보가, line이라 하면
2개의 정점 정보가, point라면 1개의 정점 정보를 참조하면서 처리하는 것이 가능해지기 때
문에 Vertex Shader보다 폭넓은 계산을 할 수 있습니다.
한가지 주의할 점은 Vertex Shader는 정점 단위로 처리하며 그 처리 정점에 대한 정보만
이 전달되지만, GeometrZ Shader는 입력용 프리미티브 형과는 관계없이 프리미티브 어⯱
블리의 토폴로지에 따라 결정되는 프리미티브 단위의 처리를 합니다. 즉, 그림 6.1과 같이
토폴로지가 Triangles인 Quad메쉬에 GeometrZ Shader를 실행할 경우 GeometrZ Shader
는 삼각형 1과 2에 대해 2번 실행됩니다. 여기서 입력용 프리미티브형을 Line으로 적용할
경우, 입력에서 넘어오는 정보는 삼각형 1에서는 0, 1, 2중에 2개의 정점, 2의 경우엔 0, 2,
3중에 2개의 정점이 넘어옵니다.



