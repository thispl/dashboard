<template>
	<!-- Tabs Section -->
	<div class="bg-white flex flex-nowrap gap-2 justify-center overflow-x-hidden items-center">
		<button
			@click="activeTab='Organisation Chart'"
			class="font-semibold w-full text-sm text-center h-8 pt-0.5 px-2"
			:class="{
				'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Organisation Chart',
			}"
		>
			Organisation Chart
		</button>

		<p>|</p>

		<button
			@click="activeTab='Total Activities Done'"
			class="font-semibold w-full text-sm text-center h-8 pt-0.5 px-2"
			:class="{
				'border-b-2 border-b-[#fba800] bg-[#fefdec]':
					activeTab === 'Total Activities Done',
			}"
		>
			Total Activities Done
		</button>

		<p>|</p>

		<button
			@click="activeTab='Maintenance'"
			class="font-semibold w-full text-sm text-center h-8 pt-0.5 px-2"
			:class="{ 'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Maintenance' }"
		>
			Maintenance
		</button>
		<p>|</p>
		<button
			@click="activeTab='HR'"
			class="font-semibold w-full text-sm text-center h-8 pt-0.5 px-2"
			:class="{ 'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'HR' }"
		>
			HR
		</button>
		<p>|</p>

		<button
			@click="activeTab='Safety'"
			class="font-semibold w-full text-sm text-center h-8 pt-0.5 px-2"
			:class="{ 'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Safety' }"
		>
			SHE
		</button>

		<p>|</p>

		<button
			@click="activeTab='Operations'"
			class="font-semibold w-full text-sm text-center h-8 pt-0.5 px-2"
			:class="{ 'border-b-2 border-b-[#fba800] bg-[#fefdec]': activeTab === 'Operations' }"
		>
			Operations
		</button>
	</div>

	<!-- Charts Section -->
	<div class="mt-4 bg-white">
		<!-- Maintenance -->
		<div v-if="activeTab === 'Maintenance'" class="bg-white pt-5 w-full">
			<div class="bg-white ml-[10px] pb-[20px] w-full flex gap-10 flex-wrap">
				<div
					v-if="overallSchvsAccDataFiltered.length"
					class="bg-white ml-[10px] pb-[20px] w-full flex gap-10 flex-wrap"
				>
					<CountCard
						:countCardData="{
							count: overallSchvsAccDataFiltered[0].completion_rate,
							title: 'PM Completion Rate',
							data: overallSchvsAccDataFiltered[0].series[1].data,
						}"
					/>

					<CountCard
						:countCardData="{
							count: overallSchvsAccDataFiltered[0].totals.Planned,
							title: 'PM Planned Total',
							data: overallSchvsAccDataFiltered[0].series[0].data,
						}"
					/>

					<CountCard
						:countCardData="{
							count: overallSchvsAccDataFiltered[0].totals.Completed,
							title: 'PM Completed Total',
							data: overallSchvsAccDataFiltered[0].per,
						}"
					/>
				</div>
				<!-- <div v-else class="text-center mt-5 text-gray-500">
                    No data available in Overall PM/CM/WR for selected filters.
                </div>     -->

				<!-- <CountCard 
                    :countCardData="{
                        count: overallSchvsAccData.completion_rate,
                        title: 'PM Outstanding Total',
                        data: overallSchvsAccData.per
                    }"
                    />    -->

				<div
					v-if="cmOverallDataFiltered.length"
					class="bg-white ml-[10px] pb-[20px] w-full flex gap-10 flex-wrap"
				>
					<CountCard
						:countCardData="{
							count: cmOverallDataFiltered[0].completion_rate,
							title: 'CM Completion Rate',
							data: cmOverallDataFiltered[0].accomplished,
						}"
					/>

					<CountCard
						:countCardData="{
							count: cmOverallDataFiltered[0].totals.scheduled,
							title: 'CM Scheduled Total',
							data: cmOverallDataFiltered[0].scheduled,
						}"
					/>

					<CountCard
						:countCardData="{
							count: cmOverallDataFiltered[0].totals.accomplished,
							title: 'CM Accomplished Total',
							data: cmOverallDataFiltered[0].accomplished,
						}"
					/>
				</div>

				<!-- <div v-else class="text-center mt-5 text-gray-500">
                    No data available in CM for selected filters.
                </div>  -->

				<div
					v-if="wrOverallDataFiltered.length"
					class="bg-white ml-[10px] pb-[20px] w-full flex gap-10 flex-wrap"
				>
					<CountCard
						:countCardData="{
							count: wrOverallDataFiltered[0].completion_rate,
							title: 'WR Completion Rate',
							data: wrOverallDataFiltered[0].accomplished,
						}"
					/>

					<CountCard
						:countCardData="{
							count: (wrOverallDataFiltered[0].total || wrOverallDataFiltered[0].totals || {}).scheduled,
							title: 'WR Scheduled Total',
							data: wrOverallDataFiltered[0].scheduled,
						}"
					/>

					<CountCard
						:countCardData="{
							count: (wrOverallDataFiltered[0].total || wrOverallDataFiltered[0].totals || {}).accomplished,
							title: 'WR Accomplished Total',
							data: wrOverallDataFiltered[0].accomplished,
						}"
					/>
				</div>
				<!-- 
                 <div v-else class="text-center mt-5 text-gray-500">
                    No data available in WR for selected filters.
                </div>  -->

				<div class="bg-white ml-[10px] pb-[20px] w-full flex gap-10 flex-wrap">
					<div v-if="roomOccupancyDataFiltered.length">
						<CountCard
							:countCardData="{
								count: overallOccupancy,
								title: 'Room Occupancy - Building wise',
								data: this.roomOccupancyDataFiltered[0].occupancyPercent.map(
									(item) => item,
								),
							}"
						/>
					</div>

					<!-- <div v-else class="text-center mt-5 text-gray-500">
                    No data available in Room Occupancy - Building wise for selected filters.
                </div>  -->

					<div v-if="roomOccupancyTypeDataFiltered.length">
						<CountCard
							:countCardData="{
								count: overallOccupancytypewise,
								title: 'Room Occupancy - Building Type wise',
								data: roomOccupancyTypeDataFiltered.map((item) => item.occupancy),
							}"
						/>
					</div>

					<!-- <div v-else class="text-center mt-5 text-gray-500">
                    No data available in Room Occupancy - Building Type wise for selected filters.
        </div>  -->
				</div>
			</div>
		</div>

		<!-- Total Activities Done -->

		<div v-if="activeTab === 'Total Activities Done'" class="bg-white pt-5 w-full">
			<div>
				<div>
					<h1 class="text-3xl font-semibold text-center mb-8 mt-5 pt-5">
						Total Activities Done
					</h1>
				</div>

				<div v-if="TotalActivitiesDataFiltered.length">
					<TotalWorkChart :chartData="TotalActivitiesDataFiltered" />
				</div>

				<div v-else class="text-center mt-5 text-gray-500">
					No data available for selected filters.
				</div>
			</div>
		</div>

		<!-- HR -->

		<div v-if="activeTab === 'HR'" class="bg-white pt-5 w-full">
			<div class="ml-[10px] pb-[20px] w-full flex gap-10">
				<div
					v-if="manpowerDetailsDataFiltered.length"
					class="bg-white ml-[10px] pb-[20px] w-full flex gap-10 flex-wrap"
				>
					<CountCard
						:countCardData="{
							count: manpowerDetailsDataFiltered[0].totals.indicative,
							title: 'ManPower Indicative Total',
							data: manpowerDetailsDataFiltered[0].series[0].data,
						}"
					/>

					<CountCard
						:countCardData="{
							count: manpowerDetailsDataFiltered[0].totals.actual,
							title: 'ManPower Actual Total',
							data: manpowerDetailsDataFiltered[0].series[1].data,
						}"
					/>
				</div>
				<!-- <div v-else class="text-center mt-5 text-gray-500">
                    No data available for selected filters.
        </div>     -->
			</div>
		</div>

		<!-- Safety  -->
		<div v-if="activeTab === 'Safety'" class="bg-white pt-5 w-full">
			<div
				v-if="safetyEnvironmentDataFiltered.length"
				class="ml-[10px] pb-[20px] w-full flex gap-10"
			>
				<CountCard
					:countCardData="{
						count: safetyEnvironmentDataFiltered[0].totals.applicable,
						title: 'Applicable',
						data: safetyEnvironmentDataFiltered[0].applicable,
					}"
				/>

				<CountCard
					:countCardData="{
						count: safetyEnvironmentDataFiltered[0].totals.actual,
						title: 'Actual',
						data: safetyEnvironmentDataFiltered[0].actual,
					}"
				/>

				<CountCard
					:countCardData="{
						count: safetyEnvironmentDataFiltered[0].totals.percentage,
						title: 'Overall Percentage',
						data: safetyEnvironmentDataFiltered[0].percentage,
					}"
				/>
			</div>

			<!-- <div v-else class="text-center mt-5 text-gray-500">
                    No data available in Safety Environment Data for selected filters.
        </div>        -->
		</div>

		<!-- Operations -->
		<div v-if="activeTab === 'Operations'" class="bg-white pt-5 w-full">
			<div class="ml-[10px] pb-[20px] w-full flex flex-wrap gap-10">
				<div v-if="gasolineConsumptionFiltered.length" class="bg-white flex gap-5">
					<CountCard
						:countCardData="{
							count: gasolineConsumptionFiltered[0].totals.gasoline91,
							title: 'GASOLINE 91 Total',
							data: gasolineConsumptionFiltered[0].series[0].data,
						}"
					/>

					<CountCard
						:countCardData="{
							count: gasolineConsumptionFiltered[0].totals.diesel,
							title: 'Diesel Total',
							data: gasolineConsumptionFiltered[0].series[1].data,
						}"
					/>
				</div>

				<!-- <div v-else class="text-center mt-5 text-gray-500">
            No data available in Gasoline Consumption for selected filters.
            </div> -->

				<!-- <div v-if="waterConsumptionFiltered.length" class="bg-white   flex gap-5 "> -->
				<CountCard
					v-if="waterConsumptionFiltered.length"
					:countCardData="{
						count: waterConsumptionFiltered[0].totals.raw,
						title: 'RAW Water Total',
						data: waterConsumptionFiltered[0].series[0].data,
					}"
				/>

				<CountCard
					v-if="waterConsumptionFiltered.length"
					:countCardData="{
						count: waterConsumptionFiltered[0].totals.sweet,
						title: 'Sweet Water Total',
						data: waterConsumptionFiltered[0].series[1].data,
					}"
				/>

				<!-- </div> -->

				<!-- <div v-else class="text-center mt-5 text-gray-500">
            No data available in Water Consumption for selected filters.
            </div> -->

				<div v-if="garbageCollectionDataFiltered.length">
					<CountCard
						:countCardData="{
							count: garbageCollectionDataFiltered[0].totals,
							title: 'Garbage Collection Total',
							data: garbageCollectionDataFiltered[0].capacities,
						}"
					/>
				</div>

				<!-- <div v-else class="text-center mt-5 text-gray-500">
            No data available in Garbage Collection for selected filters.
            </div> -->

				<div v-if="sewageWaterDataFiltered.length">
					<CountCard
						:countCardData="{
							count: sewageWaterDataFiltered[0].totals,
							title: 'Sewage Water Total (In Ltrs)',
							data: sewageWaterDataFiltered[0].capacities,
						}"
					/>
				</div>

				<!-- <div v-else class="text-center mt-5 text-gray-500">
            No data available in Sewage Water Data for selected filters.
            </div> -->
			</div>
		</div>

		<!-- Organisation Chart  -->

		<div v-if="activeTab === 'Organisation Chart'" class="bg-white pt-5 w-full">
			<!-- ORGANISATION CHART - SITE MANAGEMENT -->

			<div>
				<div>
					<h1 class="text-3xl font-semibold text-center mb-8 mt-5 pt-5">
						Organisation Chart -
						<span
							class="bg-gradient-to-t from-[#fd2b94] via-[#fba800] to-[#fd2b94] bg-clip-text text-transparent"
							>Site Management</span
						>
					</h1>
				</div>

				<div>
					<!-- <div>
                    <FlowChart :chartData="OrganisationChartData"  />
                </div> -->

					<div v-if="orgUrlDataFiltered.length" class="p-5">
						<img v-if="orgUrlDataFiltered.length" :src="orgUrlDataFiltered[0].url" />
					</div>
					<div v-else class="text-center mt-5 text-gray-500">
						No data available for selected filters.
					</div>
				</div>
			</div>
		</div>

		<div class="w-full" style="color: #666666; text-align: end">
			<p>Powered by <b style="color: #211a4b">TEAMPRO</b></p>
		</div>
	</div>
</template>

<script>
import { computed } from "vue";
import { useLiveFilterStore } from "@/stores/liveFilterStore";

import PercentageCard from "@/components/PercentageCard.vue";
import MultiSeriesChart from "@/components/chart/MultiSeriesChart.vue";
import CountCard from "@/components/CountCard.vue";
import FlowChart from "@/components/chart/FlowChart.vue";
import TotalWorkChart from "@/components/chart/TotalWorkChart.vue";
import autoScrollMixin from "@/mixins/autoScrollMixin";

export default {
	mixins: [autoScrollMixin],
	props: {
		isAutoRotateStopped: Boolean
	},
	name: "Management",
	components: { PercentageCard, MultiSeriesChart, CountCard, FlowChart, TotalWorkChart },
	computed: {
		overallOccupancy() {
			if (!this.roomOccupancyDataFiltered.length || !this.roomOccupancyDataFiltered[0]) {
				return "0";
			}

			const data = this.roomOccupancyDataFiltered[0];

			if (!data.occupiedRooms || !data.totalRooms) {
				return "0";
			}

			const totalOccupied = data.occupiedRooms.reduce((sum, item) => sum + item, 0);
			const totalRooms = data.totalRooms.reduce((sum, item) => sum + item, 0);

			if (totalRooms === 0) {
				return "0";
			}

			return ((totalOccupied / totalRooms) * 100).toFixed(0) + " %";
		},

		overallOccupancytypewise() {
			if (
				!this.roomOccupancyTypeDataFiltered.length ||
				!this.roomOccupancyTypeDataFiltered
			) {
				return "0";
			}

			const data = this.roomOccupancyTypeDataFiltered;

			let totalOccupied = 0;
			let totalRooms = 0;

			data.forEach((obj) => {
				totalOccupied += obj.occupied;
				totalRooms += obj.total;
			});

			if (totalRooms === 0) {
				return "0";
			}

			return ((totalOccupied / totalRooms) * 100).toFixed(0) + " %";
		},
	},

	setup() {
		const liveFilterStore = useLiveFilterStore();

		const overallSchvsAccDataFiltered = computed(() =>
			liveFilterStore.getDataset("overall_scheduled_vs_accomplished")
		);
		const cmOverallDataFiltered = computed(() =>
			liveFilterStore.getDataset("cm_overall_scheduled_accomplished")
		);
		const wrOverallDataFiltered = computed(() =>
			liveFilterStore.getDataset("wr_overall_schedule")
		);
		const roomOccupancyDataFiltered = computed(() =>
			liveFilterStore.getDataset("room_occupancy")
		);
		const roomOccupancyTypeDataFiltered = computed(() =>
			liveFilterStore.getDataset("room_occupancy_typewise")
		);
		const manpowerDetailsDataFiltered = computed(() =>
			liveFilterStore.getDataset("manpower_details")
		);
		const safetyEnvironmentDataFiltered = computed(() =>
			liveFilterStore.getDataset("safety_and_environment")
		);
		const gasolineConsumptionFiltered = computed(() =>
			liveFilterStore.getDataset("gasoline_consumption")
		);
		const waterConsumptionFiltered = computed(() =>
			liveFilterStore.getDataset("water_consumption")
		);
		const garbageCollectionDataFiltered = computed(() =>
			liveFilterStore.getDataset("garbage_collection")
		);
		const sewageWaterDataFiltered = computed(() =>
			liveFilterStore.getDataset("sewage_water_consumption")
		);
		const TotalActivitiesDataFiltered = computed(() =>
			liveFilterStore.getDataset("total_activities_done")
		);
		const orgUrlDataFiltered = computed(() =>
			liveFilterStore.getDataset("organisation_chart_links")
		);

		return {
			overallSchvsAccDataFiltered,
			cmOverallDataFiltered,
			wrOverallDataFiltered,
			roomOccupancyDataFiltered,
			roomOccupancyTypeDataFiltered,
			manpowerDetailsDataFiltered,
			safetyEnvironmentDataFiltered,
			gasolineConsumptionFiltered,
			waterConsumptionFiltered,
			garbageCollectionDataFiltered,
			sewageWaterDataFiltered,
			TotalActivitiesDataFiltered,
			orgUrlDataFiltered,
		};
	},
	data() {
		return {
			activeTab: "Organisation Chart",
			tabs: [
				'Organisation Chart',
				'Total Activities Done',
				'Maintenance',
				'HR',
				'Safety',
				'Operations'
			],
			childTabIndex: 0,
			childIntervalId: null,
			resumeTimeoutId: null,
		};
	}
};
</script>
