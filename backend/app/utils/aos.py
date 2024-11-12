from opensearchpy import OpenSearch, RequestsHttpConnection

from app.configs.environs import config


def get_aos_client():
    auth = (config.OPENSEARCH_ADMIN_USERNAME, config.OPENSEARCH_ADMIN_PASSWORD)
    host = config.OPENSEARCH_ENDPOINT_URL
    port = 443

    aos_client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )

    # test aos_client using nori analyzer
    query_text = """
        1392년 조선 건국 당시 숨겨진 玉璽가 2023년 서울 地下鐵 공사 현장에서 발견된다. 
        고고학자 박민준(35)과 AI 전문가 Sarah Kim(29)은 玉璽에 새겨진 비밀 코드
        '朝鮮1392#평화'를 풀어 흑산도에 숨겨진 1조원의 보물을 찾아야 한다. 그러나 
        北에서 온 비밀 요원들이 그들의 뒤를 쫓는데...
    """

    request_body = {"analyzer": "nori", "text": query_text}

    # Send the request to the _analyze endpoint
    response = aos_client.indices.analyze(body=request_body)

    for token in response["tokens"]:
        print(token["token"], end=",")

    return aos_client
