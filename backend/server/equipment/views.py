from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .utils import analyze_csv
from .models import EquipmentDataset


class UploadCSVView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        summary, df = analyze_csv(file)

        EquipmentDataset.objects.create(summary=summary)

        # keep only last 5 uploads
        if EquipmentDataset.objects.count() > 5:
            EquipmentDataset.objects.first().delete()

        return Response({
            "summary": summary,
            "data": df.to_dict(orient="records")
        })
from rest_framework.decorators import api_view

@api_view(["GET"])
def history_view(request):
    datasets = EquipmentDataset.objects.order_by("-uploaded_at")[:5]

    data = [
        {
            "id": d.id,
            "uploaded_at": d.uploaded_at,
            "summary": d.summary
        }
        for d in datasets
    ]

    return Response(data)


